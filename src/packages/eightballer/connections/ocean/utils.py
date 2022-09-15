# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------


from _codecs import escape_decode


def convert_to_bytes_format(data: str) -> bytes:
    """Converts a bytes string into bytes."""

    assert data[0:2] in ["b'", 'b"'], "Data has not the bytes literal prefix"
    bytes_data = escape_decode(data[2:-1])[0]
    assert isinstance(bytes_data, bytes), "Invalid data provided."

    return bytes_data
