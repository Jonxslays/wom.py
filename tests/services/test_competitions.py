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
from datetime import datetime
from unittest import mock

import wom
from wom import CompetitionService


@mock.patch("wom.services.competitions.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_competitions(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.search_competitions(
        title="Sick Competition",
        type=wom.CompetitionType.Classic,
        status=wom.CompetitionStatus.Ongoing,
        metric=wom.Metric.Attack,
        limit=3,
        offset=1,
    )

    generate_map.assert_called_once_with(
        title="Sick Competition",
        limit=3,
        offset=1,
        type="classic",
        status="ongoing",
        metric="attack",
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Competition])


@mock.patch("wom.services.competitions.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_competitions_defaults(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.search_competitions()

    generate_map.assert_called_once_with(
        title=None,
        limit=None,
        offset=None,
        type=None,
        status=None,
        metric=None,
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Competition])


@mock.patch("wom.services.competitions.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_details(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    with_params.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.get_details(123, metric=wom.Metric.Attack)

    generate_map.assert_called_once_with(metric="attack")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.CompetitionDetail)


@mock.patch("wom.services.competitions.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_details_no_metric(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    with_params.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.get_details(123)

    generate_map.assert_called_once_with(metric=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.CompetitionDetail)


@mock.patch("wom.services.competitions.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_top_participant_history(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.get_top_participant_history(123, metric=wom.Metric.Ranged)

    generate_map.assert_called_once_with(metric="ranged")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Top5ProgressResult])


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_create_competition(
    ok_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    starts = datetime(2024, 1, 1)
    ends = datetime(2024, 1, 8)
    await service.create_competition(
        "Slayer week",
        wom.Metric.Slayer,
        starts,
        ends,
        group_id=123,
        group_verification_code="111-111-111",
    )

    generate_map.assert_called_once_with(
        title="Slayer week",
        teams=None,
        groupId=123,
        participants=None,
        endsAt=ends.isoformat(),
        startsAt=starts.isoformat(),
        metric="slayer",
        groupVerificationCode="111-111-111",
    )
    compile.assert_called_once_with()
    http.fetch.assert_awaited_once_with(123, payload=generate_map())
    ok_or_err.assert_called_once_with(b"{}", wom.CreatedCompetitionDetail)


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_edit_competition(
    ok_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.edit_competition(123, "111-111-111", title="New title")

    generate_map.assert_called_once_with(
        title="New title",
        teams=None,
        participants=None,
        startsAt=None,
        endsAt=None,
        metric=None,
        verificationCode="111-111-111",
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map())
    ok_or_err.assert_called_once_with(b"{}", wom.Competition)


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_delete_competition(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.delete_competition(123, "111-111-111")

    generate_map.assert_called_once_with(verificationCode="111-111-111")
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), allow_http_success=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_add_participants(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.add_participants(123, "111-111-111", "Jonxslays", "Zezima")

    generate_map.assert_called_once_with(
        verificationCode="111-111-111", participants=("Jonxslays", "Zezima")
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), allow_http_success=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_remove_participants(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.remove_participants(123, "111-111-111", "Jonxslays")

    generate_map.assert_called_once_with(
        verificationCode="111-111-111", participants=("Jonxslays",)
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), allow_http_success=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_add_teams(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    team_one = wom.Team("Team 1", ["Jonxslays", "lilyuffie88"])
    team_two = wom.Team("Team 2", ["Zezima", "the old nite"])
    await service.add_teams(123, "111-111-111", team_one, team_two)

    generate_map.assert_called_once_with(
        verificationCode="111-111-111", teams=(team_one, team_two)
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), allow_http_success=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_remove_teams(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.remove_teams(123, "111-111-111", "Team 1", "Team 2")

    generate_map.assert_called_once_with(
        verificationCode="111-111-111", teamNames=("Team 1", "Team 2")
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), allow_http_success=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.competitions.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_update_outdated_participants(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = CompetitionService(http, mock.Mock())

    await service.update_outdated_participants(123, "111-111-111")

    generate_map.assert_called_once_with(verificationCode="111-111-111")
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), allow_http_success=True)
    success_or_err.assert_called_once_with(b"{}", predicate=mock.ANY)


@mock.patch("wom.services.competitions.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
async def test_get_details_csv(generate_map: mock.Mock, with_params: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"player,gained\nJonxslays,1000"
    with_params.return_value = 123
    service = CompetitionService(http, mock.Mock())

    res = await service.get_details_csv(123, team_name="Cool team")

    generate_map.assert_called_once_with(metric=None, teamName="Cool team", table=None)
    http.fetch.assert_awaited_once_with(123)
    assert res.is_ok
    assert res.unwrap() == "player,gained\nJonxslays,1000"


@mock.patch("wom.services.competitions.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
async def test_get_details_csv_error(generate_map: mock.Mock, with_params: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    error = wom.HttpErrorResponse("Not found", 404)
    http.fetch.return_value = error
    with_params.return_value = 123
    service = CompetitionService(http, mock.Mock())

    res = await service.get_details_csv(123)

    assert res.is_err
    assert res.unwrap_err() is error
