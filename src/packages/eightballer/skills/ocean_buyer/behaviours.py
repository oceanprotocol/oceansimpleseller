from typing import Any, List, Optional, Set, cast

from aea.protocols.dialogue.base import DialogueLabel
from aea.skills.base import Envelope
from aea.skills.behaviours import Behaviour, TickerBehaviour
from packages.fetchai.connections.ledger.base import \
    CONNECTION_ID as LEDGER_CONNECTION_PUBLIC_ID
from packages.fetchai.protocols.ledger_api.message import LedgerApiMessage
from packages.fetchai.protocols.oef_search.message import OefSearchMessage

from packages.eightballer.protocols.ocean.message import OceanMessage
from packages.eightballer.skills.ocean_buyer import PUBLIC_ID as SENDER_ID
from packages.eightballer.skills.ocean_buyer.dialogues import (
    FipaDialogue, LedgerApiDialogue, LedgerApiDialogues, OefSearchDialogues)
from packages.eightballer.skills.ocean_buyer.strategy import GenericStrategy

DEFAULT_MAX_PROCESSING = 120
DEFAULT_TX_INTERVAL = 2.0
DEFAULT_SEARCH_INTERVAL = 5.0
LEDGER_API_ADDRESS = str(LEDGER_CONNECTION_PUBLIC_ID)


class GenericSearchBehaviour(TickerBehaviour):
    """This class implements a search behaviour."""

    def __init__(self, **kwargs: Any):
        """Initialize the search behaviour."""
        search_interval = cast(
            float, kwargs.pop("search_interval", DEFAULT_SEARCH_INTERVAL)
        )
        super().__init__(tick_interval=search_interval, **kwargs)

    def setup(self) -> None:
        """Implement the setup for the behaviour."""
        strategy = cast(GenericStrategy, self.context.strategy)
        if strategy.is_ledger_tx:
            ledger_api_dialogues = cast(
                LedgerApiDialogues, self.context.ledger_api_dialogues
            )
            ledger_api_msg, _ = ledger_api_dialogues.create(
                counterparty=LEDGER_API_ADDRESS,
                performative=LedgerApiMessage.Performative.GET_BALANCE,
                ledger_id=strategy.ledger_id,
                address=cast(str, self.context.agent_addresses.get(strategy.ledger_id)),
            )
            self.context.outbox.put_message(message=ledger_api_msg)
        else:
            strategy.is_searching = True

    def act(self) -> None:
        """Implement the act."""
        strategy = cast(GenericStrategy, self.context.strategy)
        if not strategy.is_searching:
            return
        transaction_behaviour = cast(
            GenericTransactionBehaviour, self.context.behaviours.transaction
        )
        remaining_transactions_count = len(transaction_behaviour.waiting)
        if remaining_transactions_count > 0:
            self.context.logger.info(
                f"Transaction behaviour has {remaining_transactions_count} transactions remaining. Skipping search!"
            )
            return
        strategy.update_search_query_params()
        query = strategy.get_location_and_service_query()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.SEARCH_SERVICES,
            query=query,
        )
        self.context.outbox.put_message(message=oef_search_msg)

    def teardown(self) -> None:
        """Implement the task teardown."""


class GenericTransactionBehaviour(TickerBehaviour):
    """A behaviour to sequentially submit transactions to the blockchain."""

    def __init__(self, **kwargs: Any):
        """Initialize the transaction behaviour."""
        tx_interval = cast(
            float, kwargs.pop("transaction_interval", DEFAULT_TX_INTERVAL)
        )
        self.max_processing = cast(
            float, kwargs.pop("max_processing", DEFAULT_MAX_PROCESSING)
        )
        self.processing_time = 0.0
        self.waiting: List[FipaDialogue] = []
        self.processing: Optional[LedgerApiDialogue] = None
        self.timedout: Set[DialogueLabel] = set()
        super().__init__(tick_interval=tx_interval, **kwargs)

    def setup(self) -> None:
        """Setup behaviour."""

    def act(self) -> None:
        """Implement the act."""
        if self.processing is not None:
            if self.processing_time <= self.max_processing:
                # already processing
                self.processing_time += self.tick_interval
                return
            self._timeout_processing()
        if len(self.waiting) == 0:
            # nothing to process
            return
        self._start_processing()

    def _start_processing(self) -> None:
        """Process the next transaction."""
        fipa_dialogue = self.waiting.pop(0)
        self.context.logger.info(
            f"Processing transaction, {len(self.waiting)} transactions remaining"
        )
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_msg, ledger_api_dialogue = ledger_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=LedgerApiMessage.Performative.GET_RAW_TRANSACTION,
            terms=fipa_dialogue.terms,
        )
        ledger_api_dialogue = cast(LedgerApiDialogue, ledger_api_dialogue)
        ledger_api_dialogue.associated_fipa_dialogue = fipa_dialogue
        self.processing_time = 0.0
        self.processing = ledger_api_dialogue
        self.context.logger.info(
            f"requesting transfer transaction from ledger api for message={ledger_api_msg}..."
        )
        self.context.outbox.put_message(message=ledger_api_msg)

    def teardown(self) -> None:
        """Teardown behaviour."""

    def _timeout_processing(self) -> None:
        """Timeout processing."""
        if self.processing is None:
            return
        self.timedout.add(self.processing.dialogue_label)
        self.waiting.append(self.processing.associated_fipa_dialogue)
        self.processing_time = 0.0
        self.processing = None

    def finish_processing(self, ledger_api_dialogue: LedgerApiDialogue) -> None:
        """
        Finish processing.

        :param ledger_api_dialogue: the ledger api dialogue
        """
        if self.processing == ledger_api_dialogue:
            self.processing_time = 0.0
            self.processing = None
            return
        if ledger_api_dialogue.dialogue_label not in self.timedout:
            raise ValueError(
                f"Non-matching dialogues in transaction behaviour: {self.processing} and {ledger_api_dialogue}"
            )
        self.timedout.remove(ledger_api_dialogue.dialogue_label)
        self.context.logger.debug(
            f"Timeout dialogue in transaction processing: {ledger_api_dialogue}"
        )
        # don't reset, as another might be processing

    def failed_processing(self, ledger_api_dialogue: LedgerApiDialogue) -> None:
        """
        Failed processing.

        Currently, we retry processing indefinitely.

        :param ledger_api_dialogue: the ledger api dialogue
        """
        self.finish_processing(ledger_api_dialogue)
        self.waiting.append(ledger_api_dialogue.associated_fipa_dialogue)


class OceanC2DBehaviour(Behaviour):
    def act(self) -> None:
        """Implement the act."""
        strategy = cast(GenericStrategy, self.context.strategy)

        if strategy.is_in_flight or not strategy.is_c2d_active:
            return

        if strategy.purchased_data is not None and not strategy.has_completed_c2d_job:
            self.log.info(f"submitting the compute 2 data job!")
            self.__create_envelope(
                OceanMessage.Performative.C2D_JOB, **strategy.purchased_data
            )

        if strategy.has_completed_c2d_job:
            self.log.info(
                f"Completed the c2d demonstration... Setting strategy to download behaviour"
            )
            strategy.is_c2d_active = False
            strategy.is_processing = False

    def __create_envelope(
        self, performative: OceanMessage.Performative, **kwargs
    ) -> None:
        strategy = cast(GenericStrategy, self.context.strategy)
        receiver_id = "eightballer/ocean:0.1.0"
        msg = OceanMessage(performative=performative, **kwargs)
        msg.sender = str(SENDER_ID)
        msg.to = receiver_id
        file_upload_envolope = Envelope(
            to=receiver_id, sender=str(SENDER_ID), message=msg
        )
        self.context.outbox.put(file_upload_envolope)
        strategy.is_in_flight = True

    def setup(self) -> None:
        self.log = self.context.logger

    def teardown(self) -> None:
        pass
