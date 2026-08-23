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


async def test_get_rates_ehp_decodes_skill_configs() -> None:
    body = b"""[
        {
            "skill": "woodcutting",
            "methods": [
                {"rate": 100000, "startExp": 0, "description": "Trees"},
                {
                    "rate": 250000.5, "realRate": 260000.0,
                    "startExp": 500000, "description": "Teaks"
                }
            ],
            "bonuses": [
                {
                    "originSkill": "woodcutting", "bonusSkill": "firemaking",
                    "startExp": 0, "endExp": 200000000, "end": false, "ratio": 0.5
                }
            ]
        }
    ]"""
    service, http = _service(wom.EfficiencyService, body)

    result = await service.get_rates(wom.EfficiencyAlgorithmType.Main, wom.Metric.Ehp)

    assert result.is_ok
    configs = result.unwrap()
    config = configs[0]
    assert isinstance(config, wom.SkillMetaConfig)
    assert config.skill is wom.Metric.Woodcutting

    # An omitted realRate defaults to None; a present one decodes as a float.
    assert config.methods[0].rate == 100000.0
    assert config.methods[0].real_rate is None
    assert config.methods[1].real_rate == 260000.0

    bonus = config.bonuses[0]
    assert bonus.origin_skill is wom.Metric.Woodcutting
    assert bonus.bonus_skill is wom.Metric.Firemaking
    assert bonus.end is False
    assert bonus.max_bonus is None

    route = http.fetch.call_args.args[0]
    assert route.uri == "/efficiency/rates"
    assert route.params == {"type": "main", "metric": "ehp"}


async def test_get_rates_ehb_decodes_boss_configs() -> None:
    body = b'[{"boss": "zulrah", "rate": 35.5}, {"boss": "vorkath", "rate": 32}]'
    service, http = _service(wom.EfficiencyService, body)

    result = await service.get_rates(wom.EfficiencyAlgorithmType.Ironman, wom.Metric.Ehb)

    assert result.is_ok
    configs = result.unwrap()
    assert isinstance(configs[0], wom.BossMetaConfig)
    assert configs[0].boss is wom.Metric.Zulrah
    assert configs[0].rate == 35.5
    # An integer rate decodes into the float field.
    assert configs[1].rate == 32.0

    route = http.fetch.call_args.args[0]
    assert route.params == {"type": "ironman", "metric": "ehb"}


async def test_get_stats_decodes_real_model() -> None:
    # The counts are Postgres reltuples estimates, so integer JSON values must
    # decode into the float fields just as fractional ones do.
    body = b'{"players": 1234.5, "snapshots": 99999, "groups": 50, "competitions": 12}'
    service, http = _service(wom.GeneralService, body)

    result = await service.get_stats()

    assert result.is_ok
    stats = result.unwrap()
    assert isinstance(stats, wom.Stats)
    assert stats.players == 1234.5
    assert stats.snapshots == 99999.0
    assert stats.groups == 50.0
    assert stats.competitions == 12.0

    route = http.fetch.call_args.args[0]
    assert route.uri == "/stats"


# A snapshot as WOM sends it over the wire, including the legacy top-level
# ``id: -1`` field the API injects for backwards compatibility (which must be
# ignored, not rejected, by the Snapshot model).
_SNAPSHOT_JSON = """{
    "id": -1,
    "playerId": 42,
    "createdAt": "2024-01-01T00:00:00.000Z",
    "importedAt": null,
    "data": {
        "skills": {
            "attack": {
                "metric": "attack", "rank": 1, "level": 99,
                "experience": 200000000, "ehp": 12.3
            }
        },
        "bosses": {
            "zulrah": {"metric": "zulrah", "rank": 5, "kills": 1000, "ehb": 20.0}
        },
        "activities": {
            "last_man_standing": {
                "metric": "last_man_standing", "rank": 3, "score": 500
            }
        },
        "computed": {
            "ehp": {"metric": "ehp", "rank": 2, "value": 1234.5}
        }
    }
}"""


NAME_CHANGE_DETAIL_JSON = (
    """{
    "nameChange": {
        "id": 7,
        "playerId": 42,
        "oldName": "old guy",
        "newName": "new guy",
        "status": "pending",
        "reviewContext": null,
        "resolvedAt": null,
        "updatedAt": "2024-01-02T03:04:05.000Z",
        "createdAt": "2024-01-01T00:00:00.000Z"
    },
    "data": {
        "isNewOnHiscores": true,
        "isOldOnHiscores": false,
        "isNewTracked": false,
        "hasNegativeGains": true,
        "negativeGains": {"attack": -1000.0, "ehp": -0.5},
        "timeDiff": 3600000,
        "hoursDiff": 1.5,
        "ehpDiff": 2.5,
        "ehbDiff": 0.0,
        "oldStats": """
    + _SNAPSHOT_JSON
    + ""","newStats": """
    + _SNAPSHOT_JSON
    + """}
}"""
).encode()


async def test_get_name_change_details_decodes_nested_data() -> None:
    service, http = _service(wom.NameChangeService, NAME_CHANGE_DETAIL_JSON)

    result = await service.get_name_change_details(7)

    assert result.is_ok
    detail = result.unwrap()
    assert isinstance(detail, wom.NameChangeDetail)
    assert detail.name_change.id == 7
    assert detail.name_change.status is wom.NameChangeStatus.Pending

    data = detail.data
    assert data is not None
    # Fractional diffs decode as floats, not truncated ints.
    assert data.hours_diff == 1.5
    assert data.ehp_diff == 2.5
    assert data.has_negative_gains is True
    assert data.negative_gains == {wom.Metric.Attack: -1000.0, wom.Metric.Ehp: -0.5}

    # The nested snapshots decode fully, and the legacy ``id: -1`` field is
    # ignored rather than causing a decode error.
    assert isinstance(data.old_stats, wom.Snapshot)
    assert data.old_stats.data.skills[wom.Metric.Attack].level == 99
    assert data.new_stats is not None
    assert data.new_stats.data.bosses[wom.Metric.Zulrah].kills == 1000

    route = http.fetch.call_args.args[0]
    assert route.uri == "/names/7"


async def test_get_name_change_details_omits_data_when_absent() -> None:
    # An already-resolved change comes back with just ``{ nameChange }`` and no
    # ``data`` key; the optional field must default to None, not raise.
    body = b"""{
        "nameChange": {
            "id": 8,
            "playerId": 42,
            "oldName": "old guy",
            "newName": "new guy",
            "status": "approved",
            "reviewContext": null,
            "resolvedAt": "2024-02-02T00:00:00.000Z",
            "updatedAt": "2024-02-02T00:00:00.000Z",
            "createdAt": "2024-01-01T00:00:00.000Z"
        }
    }"""
    service, _ = _service(wom.NameChangeService, body)

    result = await service.get_name_change_details(8)

    assert result.is_ok
    detail = result.unwrap()
    assert detail.name_change.id == 8
    assert detail.data is None


async def test_bulk_submit_name_changes_decodes_result_and_posts_array() -> None:
    body = b'{"nameChangesSubmitted": 2, "message": "Successfully submitted 2/2 name changes."}'
    service, http = _service(wom.NameChangeService, body)

    result = await service.bulk_submit_name_changes([("old1", "new1"), ("old2", "new2")])

    assert result.is_ok
    bulk = result.unwrap()
    assert isinstance(bulk, wom.NameChangeBulkResult)
    assert bulk.name_changes_submitted == 2
    assert bulk.message == "Successfully submitted 2/2 name changes."

    # The body is posted as a bare JSON array of {oldName, newName} objects.
    route = http.fetch.call_args.args[0]
    assert route.uri == "/names/bulk"
    assert http.fetch.call_args.kwargs["payload"] == [
        {"oldName": "old1", "newName": "new1"},
        {"oldName": "old2", "newName": "new2"},
    ]
