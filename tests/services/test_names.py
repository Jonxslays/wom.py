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

import typing as t
from unittest import mock

import wom
from wom import NameChangeService


@mock.patch("wom.services.names.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_name_changes(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = NameChangeService(http, mock.Mock())

    await service.search_name_changes()

    generate_map.assert_called_once_with(
        username=None,
        status=None,
        limit=None,
        offset=None,
    )

    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.NameChange])


@mock.patch("wom.services.names.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_name_changes_w_username(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = NameChangeService(http, mock.Mock())

    await service.search_name_changes("EEP")

    generate_map.assert_called_once_with(
        username="EEP",
        status=None,
        limit=None,
        offset=None,
    )

    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.NameChange])


@mock.patch("wom.services.names.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_name_changes_w_status(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = NameChangeService(http, mock.Mock())

    await service.search_name_changes(status=wom.NameChangeStatus.Denied)

    generate_map.assert_called_once_with(
        username=None,
        status="denied",
        limit=None,
        offset=None,
    )

    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.NameChange])


@mock.patch("wom.services.names.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_name_changes_w_limit(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = NameChangeService(http, mock.Mock())

    await service.search_name_changes(limit=69)

    generate_map.assert_called_once_with(
        username=None,
        status=None,
        limit=69,
        offset=None,
    )

    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.NameChange])


@mock.patch("wom.services.names.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_name_changes_w_offset(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = NameChangeService(http, mock.Mock())

    await service.search_name_changes(offset=420)

    generate_map.assert_called_once_with(
        username=None,
        status=None,
        limit=None,
        offset=420,
    )

    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.NameChange])


@mock.patch("wom.services.names.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_submit_name_change(
    ok_or_err: mock.Mock, generate_map: mock.Mock, _compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    _compile.return_value = 123
    service = NameChangeService(http, mock.Mock())

    await service.submit_name_change("old", "new")

    generate_map.assert_called_once_with(oldName="old", newName="new")
    http.fetch.assert_awaited_once_with(123, payload=generate_map())
    ok_or_err.assert_called_once_with(b"[]", wom.NameChange)
