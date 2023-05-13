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

import pytest

from wom import Client
from wom import services


async def test_all_services_exist() -> None:
    client = Client()
    assert isinstance(client.competitions, services.CompetitionService)
    assert isinstance(client.deltas, services.DeltaService)
    assert isinstance(client.efficiency, services.EfficiencyService)
    assert isinstance(client.groups, services.GroupService)
    assert isinstance(client.names, services.NameChangeService)
    assert isinstance(client.players, services.PlayerService)
    assert isinstance(client.records, services.RecordService)
    await client.close()


@mock.patch("wom.client.serializer.Serializer")
@mock.patch("wom.client.services.HttpService")
async def test_basic_init(http: mock.MagicMock, serializer: mock.MagicMock) -> None:
    _ = Client()
    http.assert_called_once_with(None, None, None)
    serializer.assert_called_once()


@mock.patch("wom.client.serializer.Serializer")
@mock.patch("wom.client.services.HttpService")
async def test_full_init(http: mock.MagicMock, serializer: mock.MagicMock) -> None:
    _ = Client("abc", user_agent="ennui", api_base_url="fake")
    http.assert_called_once_with("abc", "ennui", "fake")
    serializer.assert_called_once()


@mock.patch("wom.client.services.HttpService.set_api_key")
async def test_set_api_key(set_api_key: mock.MagicMock) -> None:
    client = Client()
    client.set_api_key("hello")
    set_api_key.assert_called_once_with("hello")


@mock.patch("wom.client.services.HttpService.unset_api_key")
async def test_unset_api_key(unset_api_key: mock.MagicMock) -> None:
    client = Client()
    client.unset_api_key()
    unset_api_key.assert_called_once()


@mock.patch("wom.client.services.HttpService.set_user_agent")
async def test_set_user_agent(set_user_agent: mock.MagicMock) -> None:
    client = Client()
    client.set_user_agent("Jonxslays")
    set_user_agent.assert_called_once_with("Jonxslays")


@mock.patch("wom.client.services.HttpService.set_base_url")
async def test_set_api_base_url(set_base_url: mock.MagicMock) -> None:
    client = Client()
    client.set_api_base_url("https://localhost:6969")
    set_base_url.assert_called_once_with("https://localhost:6969")


@mock.patch("wom.client.services.HttpService.close")
async def test_close(close: mock.MagicMock) -> None:
    client = Client()
    await client.close()
    close.assert_called_once()


@mock.patch("wom.client.Client._Client__init_service")
async def test_init_service(init_service: mock.MagicMock) -> None:
    _ = Client()
    init_service.assert_has_calls(
        (
            mock.call(services.DeltaService),
            mock.call(services.GroupService),
            mock.call(services.PlayerService),
            mock.call(services.RecordService),
            mock.call(services.NameChangeService),
            mock.call(services.EfficiencyService),
            mock.call(services.CompetitionService),
        )
    )


async def test_init_service_fails() -> None:
    client = Client()

    with pytest.raises(TypeError) as e:
        client._Client__init_service(int)  # type: ignore

    assert e.exconly() == "TypeError: 'int' can not be initialized as a service."
    await client.close()
