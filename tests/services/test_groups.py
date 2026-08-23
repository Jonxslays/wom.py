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
from wom import GroupService


def test_parse_member_fragments() -> None:
    service = GroupService(mock.Mock(), mock.Mock())
    frag = wom.GroupMemberFragment("Jonxslays", wom.GroupRole.Owner)

    parsed = list(service._parse_member_fragments(["Zezima", frag]))

    assert parsed[0] == wom.GroupMemberFragment("Zezima", None)
    assert parsed[1] is frag


def test_prepare_member_fragments() -> None:
    service = GroupService(mock.Mock(), mock.Mock())
    frag = wom.GroupMemberFragment("Jonxslays", wom.GroupRole.Owner)

    prepared = service._prepare_member_fragments(["Zezima", frag])

    assert prepared == (
        {"username": "Zezima"},
        {"username": "Jonxslays", "role": "owner"},
    )


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_search_groups(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.search_groups("Some group", limit=3, offset=1)

    generate_map.assert_called_once_with(name="Some group", limit=3, offset=1)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Group])


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_details(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_details(1234)

    compile.assert_called_once_with(1234)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.GroupDetail)


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_create_group(
    ok_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    frag = wom.GroupMemberFragment("Jonxslays", wom.GroupRole.Owner)
    await service.create_group("My new group", frag, "Zezima", description="The most epic group.")

    generate_map.assert_called_once_with(
        name="My new group",
        clanChat=None,
        homeworld=None,
        description="The most epic group.",
        members=({"username": "Jonxslays", "role": "owner"}, {"username": "Zezima"}),
    )
    compile.assert_called_once_with()
    http.fetch.assert_awaited_once_with(123, payload=generate_map())
    ok_or_err.assert_called_once_with(b"{}", wom.CreatedGroupDetail)


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_edit_group(
    ok_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.edit_group(123, "111-111-111", name="My new group name")

    generate_map.assert_called_once_with(
        name="My new group name",
        clanChat=None,
        homeworld=None,
        description=None,
        verificationCode="111-111-111",
        members=None,
        socialLinks=None,
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map())
    ok_or_err.assert_called_once_with(b"{}", wom.GroupDetail)


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_edit_group_w_members_and_social_links(
    ok_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    frag = wom.GroupMemberFragment("Jonxslays", wom.GroupRole.Owner)
    social_links = wom.SocialLinks(website="https://example.com")
    await service.edit_group(
        123,
        "111-111-111",
        members=[frag, "Faabvk"],
        social_links=social_links,
    )

    generate_map.assert_called_once_with(
        name=None,
        clanChat=None,
        homeworld=None,
        description=None,
        verificationCode="111-111-111",
        members=({"username": "Jonxslays", "role": "owner"}, {"username": "Faabvk"}),
        socialLinks=social_links.to_dict(),
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map())
    ok_or_err.assert_called_once_with(b"{}", wom.GroupDetail)


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_delete_group(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.delete_group(123, "111-111-111")

    generate_map.assert_called_once_with(verificationCode="111-111-111")
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), message_response=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_add_members(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    frag = wom.GroupMemberFragment("Jonxslays", wom.GroupRole.Administrator)
    await service.add_members(123, "111-111-111", frag, "Zezima")

    generate_map.assert_called_once_with(
        verificationCode="111-111-111",
        members=({"username": "Jonxslays", "role": "administrator"}, {"username": "Zezima"}),
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), message_response=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_remove_members(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.remove_members(123, "111-111-111", "Jonxslays", "Zezima")

    generate_map.assert_called_once_with(
        verificationCode="111-111-111", members=("Jonxslays", "Zezima")
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), message_response=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_change_member_role(
    ok_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.change_member_role(123, "111-111-111", "Jonxslays", wom.GroupRole.Admiral)

    generate_map.assert_called_once_with(
        verificationCode="111-111-111", username="Jonxslays", role="admiral"
    )
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map())
    ok_or_err.assert_called_once_with(b"{}", wom.GroupMembership)


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._success_or_err")
async def test_update_outdated_members(
    success_or_err: mock.Mock, generate_map: mock.Mock, compile: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.update_outdated_members(123, "111-111-111")

    generate_map.assert_called_once_with(verificationCode="111-111-111")
    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123, payload=generate_map(), message_response=True)
    success_or_err.assert_called_once_with(b"{}")


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_competitions(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_competitions(123, limit=10, offset=2)

    generate_map.assert_called_once_with(limit=10, offset=2)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Competition])


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_gains_w_period(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_gains(123, wom.Metric.Zulrah, period=wom.Period.Week, limit=10)

    generate_map.assert_called_once_with(
        limit=10,
        offset=None,
        metric="zulrah",
        period="week",
        endDate=None,
        startDate=None,
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.GroupMemberGains])


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_gains_w_dates(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    start = datetime(2024, 1, 1)
    end = datetime(2024, 2, 1)
    await service.get_gains(123, wom.Metric.Zulrah, start_date=start, end_date=end)

    generate_map.assert_called_once_with(
        limit=None,
        offset=None,
        metric="zulrah",
        period=None,
        endDate=end.isoformat(),
        startDate=start.isoformat(),
    )
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.GroupMemberGains])


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_bulk_gains(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_bulk_gains(123, period=wom.Period.Week)

    generate_map.assert_called_once_with(period="week", endDate=None, startDate=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.BulkGroupMemberGains])


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_achievements(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_achievements(123, limit=10)

    generate_map.assert_called_once_with(limit=10, offset=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.Achievement])


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_records(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_records(123, wom.Metric.Zulrah, wom.Period.Day, limit=3)

    generate_map.assert_called_once_with(limit=3, offset=None, metric="zulrah", period="day")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.RecordLeaderboardEntry])


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_hiscores(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_hiscores(123, wom.Metric.Runecrafting, limit=10)

    generate_map.assert_called_once_with(limit=10, offset=None, metric="runecrafting")
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.GroupHiscoresEntry])


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_bulk_hiscores(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_bulk_hiscores(123)

    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.BulkGroupHiscoresEntry])


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_name_changes(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_name_changes(123, limit=10)

    generate_map.assert_called_once_with(limit=10, offset=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.NameChange])


@mock.patch("wom.services.groups.routes.Route.compile")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_statistics(ok_or_err: mock.Mock, compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"{}"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_statistics(123)

    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"{}", wom.GroupStatistics)


@mock.patch("wom.services.groups.routes.CompiledRoute.with_params")
@mock.patch("wom.services.base.BaseService._generate_map")
@mock.patch("wom.services.base.BaseService._ok_or_err")
async def test_get_activity(
    ok_or_err: mock.Mock, generate_map: mock.Mock, with_params: mock.Mock
) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"[]"
    with_params.return_value = 123
    service = GroupService(http, mock.Mock())

    await service.get_activity(69, limit=5)

    generate_map.assert_called_once_with(limit=5, offset=None)
    http.fetch.assert_awaited_once_with(123)
    ok_or_err.assert_called_once_with(b"[]", t.List[wom.GroupActivity])


@mock.patch("wom.services.groups.routes.Route.compile")
async def test_get_members_csv(compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    http.fetch.return_value = b"username,role\nJonxslays,owner"
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    res = await service.get_members_csv(123)

    compile.assert_called_once_with(123)
    http.fetch.assert_awaited_once_with(123)
    assert res.is_ok
    assert res.unwrap() == "username,role\nJonxslays,owner"


@mock.patch("wom.services.groups.routes.Route.compile")
async def test_get_members_csv_error(compile: mock.Mock) -> None:
    http = mock.Mock()
    http.fetch = mock.AsyncMock()
    error = wom.HttpErrorResponse("Not found", 404)
    http.fetch.return_value = error
    compile.return_value = 123
    service = GroupService(http, mock.Mock())

    res = await service.get_members_csv(123)

    assert res.is_err
    assert res.unwrap_err() is error
