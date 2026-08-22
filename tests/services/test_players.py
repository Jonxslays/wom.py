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
from wom import PlayerService


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_players(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.search_players("Jonxslays", limit=3, offset=1)

    generate_map.assert_called_once_with(username="Jonxslays", limit=3, offset=1)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Player])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_players_no_pagination(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.search_players("Jonxslays")

    generate_map.assert_called_once_with(username="Jonxslays", limit=None, offset=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Player])


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_update_player(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.update_player("Jonxslays")

    compile.assert_called_once_with("Jonxslays")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.PlayerDetail)


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_assert_player_type(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.assert_player_type("Jonxslays")

    compile.assert_called_once_with("Jonxslays")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.models.AssertPlayerType)


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_details(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_details("Jonxslays")

    compile.assert_called_once_with("Jonxslays")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.PlayerDetail)


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_details_by_id(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_details_by_id(1234)

    compile.assert_called_once_with(1234)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.PlayerDetail)


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_achievements(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_achievements("Jonxslays")

    compile.assert_called_once_with("Jonxslays")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Achievement])


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_achievement_progress(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_achievement_progress("Jonxslays")

    compile.assert_called_once_with("Jonxslays")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.PlayerAchievementProgress])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_competition_participations(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_competition_participations(
        "Jonxslays", limit=3, offset=1, status=wom.CompetitionStatus.Ongoing
    )

    generate_map.assert_called_once_with(status="ongoing", offset=1, limit=3)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.PlayerParticipation])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_competition_participations_defaults(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_competition_participations("Jonxslays")

    generate_map.assert_called_once_with(status=None, offset=None, limit=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.PlayerParticipation])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_competition_standings(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_competition_standings("Jonxslays", wom.CompetitionStatus.Finished)

    generate_map.assert_called_once_with(status="finished")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.PlayerCompetitionStanding])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_group_memberships(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_group_memberships("Jonxslays", limit=3, offset=1)

    generate_map.assert_called_once_with(limit=3, offset=1)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.PlayerMembership])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_gains_w_period(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_gains("Jonxslays", period=wom.Period.Day)

    generate_map.assert_called_once_with(period="day", startDate=None, endDate=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.PlayerGains)


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_gains_w_dates(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    start = datetime(2024, 1, 1)
    end = datetime(2024, 2, 1)
    await service.get_gains("Jonxslays", start_date=start, end_date=end)

    generate_map.assert_called_once_with(
        period=None, startDate=start.isoformat(), endDate=end.isoformat()
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.PlayerGains)


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_records(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_records("Jonxslays", period=wom.Period.Week, metric=wom.Metric.Attack)

    generate_map.assert_called_once_with(period="week", metric="attack")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Record])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_records_defaults(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_records("Jonxslays")

    generate_map.assert_called_once_with(period=None, metric=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Record])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_snapshots(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_snapshots("Jonxslays", period=wom.Period.Week, limit=3, offset=1)

    generate_map.assert_called_once_with(
        period="week", startDate=None, endDate=None, limit=3, offset=1
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Snapshot])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_snapshots_w_dates(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    start = datetime(2024, 1, 1)
    end = datetime(2024, 2, 1)
    await service.get_snapshots("Jonxslays", start_date=start, end_date=end)

    generate_map.assert_called_once_with(
        period=None,
        startDate=start.isoformat(),
        endDate=end.isoformat(),
        limit=None,
        offset=None,
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Snapshot])


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_name_changes(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_name_changes("Jonxslays")

    compile.assert_called_once_with("Jonxslays")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.NameChange])


@mock.patch("wom.services.players.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_snapshots_timeline(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_snapshots_timeline("Jonxslays", wom.Metric.Attack, period=wom.Period.Week)

    generate_map.assert_called_once_with(
        period="week", startDate=None, endDate=None, metric="attack"
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.SnapshotTimelineEntry])


@mock.patch("wom.services.players.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_archives(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    compile.return_value = 123
    service = PlayerService(http, mock.Mock())

    await service.get_archives("Jonxslays")

    compile.assert_called_once_with("Jonxslays")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.PlayerArchive])
