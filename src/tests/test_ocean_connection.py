#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import asyncio
import os
from aea.mail.base import Envelope
from aea.configurations.base import ConnectionConfig

from packages.eightballer.connections.ocean.connection import OceanConnection
from packages.eightballer.protocols.ocean.message import OceanMessage
from mock import patch, Mock
from ocean_lib.models.datatoken import Datatoken

from src.tests.utils import _seller_wallet, _buyer_wallet


@patch.object(OceanConnection, "put_envelope")
def test_datatoken_creation(put_envelope):
    """Tests that _deploy_datatoken function works as expected."""

    def side_effect(envelope):
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_D2C,
        _body={
            "data_nft_name": "data_nft_c2d",
            "datatoken_name": "datatoken_c2d",
            "amount_to_mint": 100,
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_deploy_algorithm(put_envelope):
    """Tests that _deploy_algorithm function works as expected."""

    def side_effect(envelope):
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_ALGORITHM,
        _body={
            "data_nft_name": "algo_nft_c2d",
            "datatoken_name": "algo_token",
            "amount_to_mint": 100,
            "language": "python",
            "format": "docker-image",
            "version": "0.1",
            "entrypoint": "python $ALGO",
            "image": "oceanprotocol/algo_dockers",
            "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/trentmc/branin/main/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_permission_dataset(put_envelope):
    """Tests that _permission_dataset function works as expected."""
    global data_ddo
    global algo_ddo

    def side_effect(envelope):
        global data_ddo
        data_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_D2C,
        _body={
            "data_nft_name": "data_nft_c2d",
            "datatoken_name": "datatoken_c2d",
            "amount_to_mint": 100,
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    def side_effect(envelope):
        global algo_ddo
        algo_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_ALGORITHM,
        _body={
            "data_nft_name": "algo_nft_c2d",
            "datatoken_name": "algo_token",
            "amount_to_mint": 100,
            "language": "python",
            "format": "docker-image",
            "version": "0.1",
            "entrypoint": "python $ALGO",
            "image": "oceanprotocol/algo_dockers",
            "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/trentmc/branin/main/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.PERMISSION_DATASET,
        _body={"algo_did": algo_ddo, "data_did": data_ddo},
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    def side_effect(envelope):
        assert envelope.message.type == "permissions"
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_create_fixed_rate(put_envelope):
    """Tests that _deploy_algorithm & _create_fixed_rate functions work as expected."""
    global data_ddo
    global algo_ddo

    def side_effect(envelope):
        global data_ddo
        data_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_D2C,
        _body={
            "data_nft_name": "data_nft_c2d",
            "datatoken_name": "datatoken_c2d",
            "amount_to_mint": 100,
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    def side_effect(envelope):
        global algo_ddo
        algo_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_ALGORITHM,
        _body={
            "data_nft_name": "algo_nft_c2d",
            "datatoken_name": "algo_token",
            "amount_to_mint": 100,
            "language": "python",
            "format": "docker-image",
            "version": "0.1",
            "entrypoint": "python $ALGO",
            "image": "oceanprotocol/algo_dockers",
            "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/trentmc/branin/main/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.PERMISSION_DATASET,
        _body={"algo_did": algo_ddo, "data_did": data_ddo},
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    def side_effect(envelope):
        global datatoken_address
        datatoken_address = envelope.message.datatoken_contract_address
        assert envelope.message.type == "permissions"
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.CREATE_POOL,
        _body={
            "datatoken_address": datatoken_address,
            "rate": 1,
            "ocean_amt": 10,
        },
    )

    def side_effect(envelope):
        assert (
            envelope.message.performative
            == OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_purchase_datatoken(put_envelope, caplog):
    """Tests that _purchase_datatoken function works as expected as buyer role."""
    global data_ddo
    global algo_ddo
    global pool_address

    def side_effect(envelope):
        global data_ddo
        data_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_D2C,
        _body={
            "data_nft_name": "data_nft_c2d",
            "datatoken_name": "datatoken_c2d",
            "amount_to_mint": 100,
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    def side_effect(envelope):
        global algo_ddo
        algo_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_ALGORITHM,
        _body={
            "data_nft_name": "algo_nft_c2d",
            "datatoken_name": "algo_token",
            "amount_to_mint": 100,
            "language": "python",
            "format": "docker-image",
            "version": "0.1",
            "entrypoint": "python $ALGO",
            "image": "oceanprotocol/algo_dockers",
            "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/trentmc/branin/main/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.PERMISSION_DATASET,
        _body={"algo_did": algo_ddo, "data_did": data_ddo},
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    def side_effect(envelope):
        global datatoken_address
        datatoken_address = envelope.message.datatoken_contract_address
        assert envelope.message.type == "permissions"
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.CREATE_POOL,
        _body={
            "datatoken_address": datatoken_address,
            "rate": 1,
            "ocean_amt": 10,
        },
    )

    def side_effect(envelope):
        global pool_address
        pool_address = envelope.message.pool_address
        assert (
            envelope.message.performative
            == OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    ocean2 = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
            key_path=os.environ["BUYER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop2 = asyncio.get_event_loop()
    loop2.run_until_complete(ocean2.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DOWNLOAD_JOB,
        _body={
            "datatoken_address": datatoken_address,
            "datatoken_amt": 2,
            "max_cost_ocean": 5,
            "asset_did": data_ddo,
            "pool_address": pool_address,
        },
    )

    def side_effect(envelope):
        assert envelope.message.performative == OceanMessage.Performative.DOWNLOAD_JOB

    put_envelope.side_effect = side_effect
    ocean2.on_connect()

    seller_wallet = _seller_wallet(ocean2)
    buyer_wallet = _buyer_wallet(ocean2)
    datatoken = Datatoken(ocean2.ocean.web3, datatoken_address)
    OCEAN_token = ocean2.ocean.OCEAN_token
    assert OCEAN_token.balanceOf(seller_wallet.address) > 0
    if OCEAN_token.balanceOf(buyer_wallet.address) == 0:
        OCEAN_token.transfer(
            buyer_wallet.address, ocean2.ocean.to_wei(50), seller_wallet
        )
    assert OCEAN_token.balanceOf(buyer_wallet.address) > 0

    datatoken.mint(buyer_wallet.address, ocean2.ocean.to_wei(50), seller_wallet)
    assert datatoken.balanceOf(buyer_wallet.address) > 0

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean2.on_send(envelope)
