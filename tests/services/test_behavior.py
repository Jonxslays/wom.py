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

"""Behavior-level service tests.

Unlike the per-method tests that mock ``_generate_map`` / ``_ok_or_err`` and
assert internal wiring, these drive a service through the *real* serializer and
the *real* ``BaseService`` helpers, faking only the network boundary
(``HttpService.fetch``). They verify what a caller actually observes: real
decoded models, camelCase -> snake_case mapping, param generation, and the
``Ok``/``Err`` contract.
"""

from __future__ import annotations

import typing as t
from datetime import datetime
from datetime import timezone
from unittest import mock

import wom


def _service(cls: t.Any, fetch_return: t.Any) -> t.Tuple[t.Any, mock.Mock]:
    """Build a service backed by a real serializer, faking only the network."""
    http = mock.Mock()
    http.fetch = mock.AsyncMock(return_value=fetch_return)
    return cls(http, wom.Serializer()), http


NAME_CHANGE_JSON = b"""[
    {
        "id": 1,
        "playerId": 42,
        "oldName": "old guy",
        "newName": "new guy",
        "status": "approved",
        "reviewContext": null,
        "resolvedAt": "2024-01-02T03:04:05.000Z",
        "updatedAt": "2024-01-02T03:04:05.000Z",
        "createdAt": "2024-01-01T00:00:00.000Z"
    }
]"""


async def test_search_name_changes_decodes_real_model() -> None:
    service, http = _service(wom.NameChangeService, NAME_CHANGE_JSON)

    result = await service.search_name_changes(status=wom.NameChangeStatus.Denied, limit=1)

    # A real Ok wrapping a real, fully decoded model - no helper was mocked.
    assert result.is_ok
    changes = result.unwrap()
    assert len(changes) == 1
    change = changes[0]
    assert isinstance(change, wom.NameChange)
    assert change.id == 1
    assert change.player_id == 42  # camelCase -> snake_case really happened
    assert change.old_name == "old guy"
    assert change.new_name == "new guy"
    assert change.status is wom.NameChangeStatus.Approved
    assert change.review_context is None
    assert change.created_at == datetime(2024, 1, 1, tzinfo=timezone.utc)

    # The real _generate_map dropped the None params, and the enum survives as
    # a query param that stringifies to its API value.
    route = http.fetch.call_args.args[0]
    assert route.uri == "/names"
    assert set(route.params) == {"status", "limit"}
    assert str(route.params["status"]) == "denied"
    assert route.params["limit"] == 1


async def test_search_name_changes_err_passes_through_without_raising() -> None:
    error = wom.HttpErrorResponse("Player not found", 404, "NOT_FOUND")
    service, _ = _service(wom.NameChangeService, error)

    result = await service.search_name_changes("nobody")

    # The Result contract: API errors become Err, never exceptions.
    assert result.is_err
    assert result.unwrap_err() is error


async def test_delete_group_success_message_is_wrapped_in_ok() -> None:
    success = wom.HttpSuccessResponse("Successfully deleted group.")
    success.status = 200
    service, http = _service(wom.GroupService, success)

    result = await service.delete_group(123, "111-111-111")

    assert result.is_ok
    assert result.unwrap().message == "Successfully deleted group."

    # The route was compiled with the real id, and the payload/flag were wired
    # through to the http layer.
    route = http.fetch.call_args.args[0]
    assert route.uri == "/groups/123"
    assert http.fetch.call_args.kwargs["payload"] == {"verificationCode": "111-111-111"}
    assert http.fetch.call_args.kwargs["message_response"] is True
