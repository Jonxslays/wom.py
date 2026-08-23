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

import wom
from wom import GeneralService


@mock.patch("wom.services.general.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_stats(ok_or_err: mock.Mock, _compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    _compile.return_value = 123
    service = GeneralService(http, mock.Mock())

    await service.get_stats()

    _compile.assert_called_once_with()
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.Stats)
