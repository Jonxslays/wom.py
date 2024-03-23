# wom.py - An asynchronous wrapper for the Wise Old Man API.
# Copyright (c) 2023-present Jonxslays
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from unittest import mock

from wom import HttpErrorResponse
from wom import HttpService
from wom import constants


def test_basic_init() -> None:
    service = HttpService(None, None, None)

    assert service._base_url == constants.WOM_BASE_URL  # type: ignore
    assert service._headers == {  # type: ignore
        "x-user-agent": constants.DEFAULT_USER_AGENT,
        "User-Agent": constants.DEFAULT_USER_AGENT,
    }


def test_full_init() -> None:
    service = HttpService("xxx", "lolol", "https://WUTTTT")

    assert service._base_url == "https://WUTTTT"  # type: ignore
    assert service._headers == {  # type: ignore
        "x-user-agent": f"{constants.USER_AGENT_BASE} lolol",
        "User-Agent": f"{constants.USER_AGENT_BASE} lolol",
        "x-api-key": "xxx",
    }


@mock.patch("wom.services.http.aiohttp.ClientResponse")
@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_read_content(_: mock.MagicMock, client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    read_bytes = mock.AsyncMock()
    client_response.content.read = read_bytes

    await service._read_content(client_response)  # type: ignore

    read_bytes.assert_awaited_once()


@mock.patch("wom.services.http.aiohttp.ClientResponse")
@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_read_content_fails(_: mock.MagicMock, client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    read_bytes = mock.AsyncMock(side_effect=Exception)
    client_response.content.read = read_bytes
    client_response.status = 500

    result = await service._read_content(client_response)  # type: ignore

    read_bytes.assert_awaited_once()
    assert isinstance(result, HttpErrorResponse)
    assert result.status == 500
    assert result.message == "Failed to read response content."


# TODO: Add more http tests here for the public methods and also with mocks for:
#   - fetch
#   - _get_request_func
#   - _init_session
#   - _request
