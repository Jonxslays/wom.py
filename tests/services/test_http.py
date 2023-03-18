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

import pytest
from unittest import mock

from wom import constants
from wom import HttpService
from wom import HttpErrorResponse


@mock.patch("wom.services.http.aiohttp.ClientSession")
def test_basic_init(client_session: mock.MagicMock) -> None:
    service = HttpService(None, None, None)

    client_session.assert_called_once()
    assert len(service._method_mapping) == 5  # type: ignore
    assert service._base_url == constants.WOM_BASE_URL  # type: ignore
    assert service._headers == {"x-user-agent": constants.DEFAULT_USER_AGENT}  # type: ignore


@mock.patch("wom.services.http.aiohttp.ClientSession")
def test_full_init(client_session: mock.MagicMock) -> None:
    service = HttpService("xxx", "lolol", "https://WUTTTT")

    client_session.assert_called_once()
    assert len(service._method_mapping) == 5  # type: ignore
    assert service._base_url == "https://WUTTTT"  # type: ignore
    assert service._headers == {  # type: ignore
        "x-user-agent": f"{constants.USER_AGENT_BASE} lolol",
        "x-api-key": "xxx",
    }


@mock.patch("wom.services.http.aiohttp.ClientResponse")
@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_try_get_json(_: mock.MagicMock, client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    response_json = mock.AsyncMock()
    client_response.json = response_json

    await service._try_get_json(client_response)  # type: ignore

    response_json.assert_awaited_once()


@mock.patch("wom.services.http.aiohttp.ClientResponse")
@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_try_get_json_fails(_: mock.MagicMock, client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    response_json = mock.AsyncMock(side_effect=Exception)
    client_response.json = response_json
    client_response.status = 404

    result = await service._try_get_json(client_response)  # type: ignore

    response_json.assert_awaited_once()
    assert isinstance(result, HttpErrorResponse)
    assert result.status == 404
    assert result.message == "Unable to deserialize response, the api is likely down."
