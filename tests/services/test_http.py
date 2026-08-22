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

import msgspec
import pytest

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


@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_get_request_func(session: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    get = mock.Mock()
    session.return_value.get = get

    await service.start()
    result = service._get_request_func("GET")  # type: ignore

    session.assert_called_once()
    assert result is get


@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_get_request_func_fails_w_no_start(session: mock.MagicMock) -> None:
    service = HttpService(None, None, None)

    with pytest.raises(RuntimeError) as e:
        _ = service._get_request_func("GET")  # type: ignore

    session.assert_not_called()
    assert e.exconly() == "RuntimeError: HttpService.start was never called, aborting..."


@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_get_request_func_fails_w_invalid_method(session: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    await service.start()

    with pytest.raises(KeyError) as e:
        _ = service._get_request_func("EEP")  # type: ignore

    session.assert_called_once()
    assert e.exconly() == "KeyError: 'EEP'"


@mock.patch("wom.services.http.aiohttp.ClientResponse")
async def test_request_error_captures_code(client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    client_response.ok = False
    client_response.status = 404
    client_response.content.read = mock.AsyncMock(
        return_value=msgspec.json.encode(
            {"message": "Player not found", "code": "PLAYER_NOT_FOUND"}
        )
    )
    req = mock.AsyncMock(return_value=client_response)

    result = await service._request(req, "https://wut")  # type: ignore

    assert isinstance(result, HttpErrorResponse)
    assert result.status == 404
    assert result.message == "Player not found"
    assert result.code == "PLAYER_NOT_FOUND"


@mock.patch("wom.services.http.aiohttp.ClientResponse")
async def test_request_error_without_code_is_none(client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    client_response.ok = False
    client_response.status = 429
    client_response.content.read = mock.AsyncMock(
        return_value=msgspec.json.encode({"message": "Too Many Requests."})
    )
    req = mock.AsyncMock(return_value=client_response)

    result = await service._request(req, "https://wut")  # type: ignore

    assert isinstance(result, HttpErrorResponse)
    assert result.status == 429
    assert result.message == "Too Many Requests."
    assert result.code is None


def test_error_response_decodes_without_code_field() -> None:
    # Proves the new optional field is non-breaking: a body lacking "code"
    # still decodes and leaves the field defaulted to None.
    decoder = msgspec.json.Decoder(HttpErrorResponse)

    result = decoder.decode(msgspec.json.encode({"message": "boom", "status": 500}))

    assert result.message == "boom"
    assert result.status == 500
    assert result.code is None


def test_error_response_positional_construction_unchanged() -> None:
    # Existing positional/keyword construction must keep working (non-breaking).
    result = HttpErrorResponse("boom", 500)

    assert result.message == "boom"
    assert result.status == 500
    assert result.code is None


@mock.patch("wom.services.http.aiohttp.ClientResponse")
async def test_request_returns_content_on_success(client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    client_response.ok = True
    client_response.content.read = mock.AsyncMock(return_value=b"[]")
    req = mock.AsyncMock(return_value=client_response)

    result = await service._request(req, "https://wut")  # type: ignore

    assert result == b"[]"


@mock.patch("wom.services.http.aiohttp.ClientResponse")
async def test_request_returns_error_on_read_failure(client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    client_response.status = 500
    client_response.content.read = mock.AsyncMock(side_effect=Exception)
    req = mock.AsyncMock(return_value=client_response)

    result = await service._request(req, "https://wut")  # type: ignore

    assert isinstance(result, HttpErrorResponse)
    assert result.status == 500
    assert result.message == "Failed to read response content."


@mock.patch("wom.services.http.aiohttp.ClientResponse")
async def test_request_allow_http_success(client_response: mock.MagicMock) -> None:
    service = HttpService(None, None, None)
    client_response.ok = True
    client_response.status = 200
    client_response.content.read = mock.AsyncMock(
        return_value=msgspec.json.encode({"message": "Success!"})
    )
    req = mock.AsyncMock(return_value=client_response)

    result = await service._request(req, "https://wut", allow_http_success=True)  # type: ignore

    assert isinstance(result, HttpErrorResponse)
    assert result.status == 200
    assert result.message == "Success!"


def test_set_api_key() -> None:
    service = HttpService(None, None, None)

    service.set_api_key("newkey")

    assert service._headers["x-api-key"] == "newkey"  # type: ignore


def test_unset_api_key() -> None:
    service = HttpService("startkey", None, None)

    service.unset_api_key()

    assert "x-api-key" not in service._headers  # type: ignore


def test_unset_api_key_when_absent() -> None:
    service = HttpService(None, None, None)

    service.unset_api_key()

    assert "x-api-key" not in service._headers  # type: ignore


def test_set_user_agent() -> None:
    service = HttpService(None, None, None)

    service.set_user_agent("my agent")

    assert service._headers["x-user-agent"] == "my agent"  # type: ignore
    assert service._headers["User-Agent"] == "my agent"  # type: ignore


def test_set_base_url() -> None:
    service = HttpService(None, None, None)

    service.set_base_url("https://new-base")

    assert service._base_url == "https://new-base"  # type: ignore


@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_start_is_idempotent(session: mock.MagicMock) -> None:
    service = HttpService(None, None, None)

    await service.start()
    await service.start()

    session.assert_called_once()


@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_close(session: mock.MagicMock) -> None:
    close = mock.AsyncMock()
    session.return_value.close = close
    session.return_value.closed = False
    service = HttpService(None, None, None)
    await service.start()

    await service.close()

    close.assert_awaited_once()


async def test_close_when_never_started() -> None:
    service = HttpService(None, None, None)

    # Should not raise even though no session was ever created.
    await service.close()


@mock.patch("wom.services.http.aiohttp.ClientSession")
async def test_close_when_already_closed(session: mock.MagicMock) -> None:
    close = mock.AsyncMock()
    session.return_value.close = close
    session.return_value.closed = True
    service = HttpService(None, None, None)
    await service.start()

    await service.close()

    close.assert_not_awaited()


@mock.patch.object(HttpService, "_get_request_func")
@mock.patch.object(HttpService, "_request", new_callable=mock.AsyncMock)
async def test_fetch(request: mock.AsyncMock, get_request_func: mock.Mock) -> None:
    service = HttpService(None, None, None)
    request.return_value = b"[]"
    reqfunc = mock.Mock()
    get_request_func.return_value = reqfunc
    route = mock.Mock()
    route.method = "GET"
    route.uri = "/players/Jonxslays"
    route.params = {"limit": 3}

    result = await service.fetch(route)

    assert result == b"[]"
    get_request_func.assert_called_once_with("GET")
    request.assert_awaited_once_with(
        reqfunc,
        constants.WOM_BASE_URL + "/players/Jonxslays",
        False,
        headers=service._headers,  # type: ignore
        params={"limit": 3},
        json=None,
    )


@mock.patch.object(HttpService, "_get_request_func")
@mock.patch.object(HttpService, "_request", new_callable=mock.AsyncMock)
async def test_fetch_w_payload_and_allow_http_success(
    request: mock.AsyncMock, get_request_func: mock.Mock
) -> None:
    service = HttpService(None, None, None)
    request.return_value = b"{}"
    reqfunc = mock.Mock()
    get_request_func.return_value = reqfunc
    route = mock.Mock()
    route.method = "POST"
    route.uri = "/groups"
    route.params = {}

    result = await service.fetch(route, payload={"name": "x"}, allow_http_success=True)

    assert result == b"{}"
    request.assert_awaited_once_with(
        reqfunc,
        constants.WOM_BASE_URL + "/groups",
        True,
        headers=service._headers,  # type: ignore
        params={},
        json={"name": "x"},
    )


# TODO: Add more http tests here with mocks for:
#   - _init_session
