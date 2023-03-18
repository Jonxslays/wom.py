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

import pytest

from wom import models
from wom import Activities
from wom import Bosses
from wom import ComputedMetrics
from wom import Serializer
from wom import Skills


@pytest.fixture()
def blank_class() -> t.Any:
    class BlankClass:
        ...

    return BlankClass


def _player_dict() -> dict[str, t.Any]:
    return {
        "id": 151063,
        "username": "zezimas bro",
        "displayName": "Zezimas bro",
        "type": "regular",
        "build": "main",
        "country": None,
        "flagged": False,
        "exp": 330940032,
        "ehp": 1057.05253,
        "ehb": 126.50192,
        "ttm": 0,
        "tt200m": 12467.36769,
        "registeredAt": "2021-01-29T01:18:41.641Z",
        "updatedAt": "2022-10-01T17:02:03.360Z",
        "lastChangedAt": "2022-10-01T17:02:03.129Z",
        "lastImportedAt": "2022-10-01T17:02:03.100Z",
    }


@pytest.fixture()
def player_dict() -> dict[str, t.Any]:
    return _player_dict()


def _deserialized_player() -> models.Player:
    player = models.Player()
    player.id = 151063
    player.username = "zezimas bro"
    player.display_name = "Zezimas bro"
    player.type = models.PlayerType.Regular
    player.build = models.PlayerBuild.Main
    player.country = None
    player.flagged = False
    player.exp = 330940032
    player.ehp = 1057.05253
    player.ehb = 126.50192
    player.ttm = 0
    player.tt200m = 12467.36769
    player.registered_at = datetime(2021, 1, 29, 1, 18, 41, 641000)
    player.updated_at = datetime(2022, 10, 1, 17, 2, 3, 360000)
    player.last_changed_at = datetime(2022, 10, 1, 17, 2, 3, 129000)
    player.last_imported_at = datetime(2022, 10, 1, 17, 2, 3, 100000)
    return player


@pytest.fixture()
def deserialized_player() -> models.Player:
    return _deserialized_player()


def _boss_dict() -> dict[str, t.Any]:
    return {"metric": "abyssal_sire", "kills": -1, "rank": -1, "ehb": 0}


@pytest.fixture()
def boss_dict() -> dict[str, t.Any]:
    return _boss_dict()


def _deserialized_boss() -> models.Boss:
    boss = models.Boss()
    boss.metric = Bosses.AbyssalSire
    boss.rank = -1
    boss.kills = -1
    boss.ehb = 0
    return boss


@pytest.fixture()
def deserialized_boss() -> models.Boss:
    return _deserialized_boss()


def _skill_dict() -> dict[str, t.Any]:
    return {
        "metric": "overall",
        "experience": 27957906,
        "rank": 948821,
        "level": 1422,
        "ehp": 118.1123000000007,
    }


@pytest.fixture()
def skill_dict() -> dict[str, t.Any]:
    return _skill_dict()


def _deserialized_skill() -> models.Skill:
    skill = models.Skill()
    skill.metric = Skills.Overall
    skill.experience = 27957906
    skill.rank = 948821
    skill.level = 1422
    skill.ehp = 118.1123000000007
    return skill


@pytest.fixture()
def deserialized_skill() -> models.Skill:
    return _deserialized_skill()


def _activity_dict() -> dict[str, t.Any]:
    return {
        "metric": "bounty_hunter_hunter",
        "score": -1,
        "rank": -1,
    }


@pytest.fixture()
def activity_dict() -> dict[str, t.Any]:
    return _activity_dict()


def _deserialized_activity() -> models.Activity:
    activity = models.Activity()
    activity.metric = Activities.BountyHunterHunter
    activity.score = -1
    activity.rank = -1
    return activity


@pytest.fixture()
def deserialized_activity() -> models.Activity:
    return _deserialized_activity()


def _computed_dict() -> dict[str, t.Any]:
    return {"metric": "ehp", "value": 118.1123000000007, "rank": 289382}


@pytest.fixture()
def computed_dict() -> dict[str, t.Any]:
    return _computed_dict()


def _deserialized_computed() -> models.ComputedMetric:
    computed = models.ComputedMetric()
    computed.metric = ComputedMetrics.Ehp
    computed.value = 118.1123000000007
    computed.rank = 289382
    return computed


@pytest.fixture()
def deserialized_computed() -> models.ComputedMetric:
    return _deserialized_computed()


def _snapshot_data_dict() -> dict[str, t.Any]:
    return {
        "skills": {"overall": _skill_dict()},
        "bosses": {"abyssal_sire": _boss_dict()},
        "activities": {"bounty_hunter_hunter": _activity_dict()},
        "computed": {"ehp": _computed_dict()},
    }


@pytest.fixture()
def snapshot_data_dict() -> dict[str, t.Any]:
    return _snapshot_data_dict()


def _deserialized_snapshot_data() -> models.SnapshotData:
    model = models.SnapshotData()

    skill = _deserialized_skill()
    boss = _deserialized_boss()
    activity = _deserialized_activity()
    computed = _deserialized_computed()

    model.skills = {skill.metric: skill}
    model.bosses = {boss.metric: boss}
    model.activities = {activity.metric: activity}
    model.computed = {computed.metric: computed}

    return model


@pytest.fixture()
def deserialized_snapshot_data() -> models.SnapshotData:
    return _deserialized_snapshot_data()


def _snapshot_dict() -> dict[str, t.Any]:
    return {
        "id": 68052294,
        "playerId": 151063,
        "createdAt": "2022-10-27T11:44:11.057Z",
        "importedAt": None,
        "data": _snapshot_data_dict(),
    }


@pytest.fixture()
def snapshot_dict() -> dict[str, t.Any]:
    return _snapshot_dict()


def _deserialized_snapshot() -> models.Snapshot:
    model = models.Snapshot()

    model.id = 68052294
    model.player_id = 151063
    model.created_at = datetime(2022, 10, 27, 11, 44, 11, 57000)
    model.imported_at = None
    model.data = _deserialized_snapshot_data()

    return model


@pytest.fixture()
def deserialized_snapshot() -> models.Snapshot:
    return _deserialized_snapshot()


def _player_detail_dict() -> dict[str, t.Any]:
    return {
        **_player_dict(),
        "combatLevel": 126,
        "latestSnapshot": _snapshot_dict(),
    }


@pytest.fixture()
def player_detail_dict() -> dict[str, t.Any]:
    return _player_detail_dict()


def _deserialized_player_detail() -> models.PlayerDetail:
    model = models.PlayerDetail()
    model.combat_level = 126
    model.player = _deserialized_player()
    model.latest_snapshot = _deserialized_snapshot()
    return model


@pytest.fixture()
def deserialized_player_detail() -> models.PlayerDetail:
    return _deserialized_player_detail()


def _assert_player_type_dict() -> dict[str, t.Any]:
    return {"player": _player_dict(), "changed": True}


@pytest.fixture()
def assert_player_type_dict() -> dict[str, t.Any]:
    return _assert_player_type_dict()


def _deserialized_assert_player_type() -> models.AssertPlayerType:
    model = models.AssertPlayerType()
    model.player = _deserialized_player()
    model.changed = True
    return model


@pytest.fixture()
def deserialized_assert_player_type() -> models.AssertPlayerType:
    return _deserialized_assert_player_type()


def test_dt_from_iso() -> None:
    serializer = Serializer()
    iso_string = "2023-03-17T17:56:31.436179"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso(iso_string)  # type: ignore
    assert expected == result


def test_dt_from_iso_with_z() -> None:
    serializer = Serializer()
    iso_string = "2023-03-17T17:56:31.436179Z"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso(iso_string)  # type: ignore
    assert expected == result


def test_dt_from_iso_maybe() -> None:
    serializer = Serializer()
    iso_string = "2023-03-17T17:56:31.436179"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso_maybe(iso_string)  # type: ignore
    assert result == expected


def test_dt_from_iso_maybe_with_z() -> None:
    serializer = Serializer()
    iso_string = "2023-03-17T17:56:31.436179Z"

    expected = datetime(2023, 3, 17, 17, 56, 31, 436179)
    result = serializer._dt_from_iso_maybe(iso_string)  # type: ignore
    assert result == expected


def test_dt_from_iso_maybe_none() -> None:
    serializer = Serializer()
    result = serializer._dt_from_iso_maybe(None)  # type: ignore
    assert result == None


def test_to_camel_case() -> None:
    serializer = Serializer()
    result = serializer._to_camel_case("test")  # type: ignore
    assert result == "test"


def test_to_camel_case_with_casing() -> None:
    serializer = Serializer()
    result = serializer._to_camel_case("test_what_im_doing")  # type: ignore
    assert result == "testWhatImDoing"


def test_map() -> None:
    serializer = Serializer()
    data = [
        {"metric": Bosses.Zulrah, "rank": 1000, "kills": 10000, "ehb": 6},
        {"metric": Bosses.Vorkath, "rank": 501, "kills": 23445, "ehb": 5},
    ]

    result = serializer._Serializer__map(serializer.deserialize_boss, data)  # type: ignore
    expected: dict[Bosses, models.Boss | int] = {}

    for i in range(2):
        boss = models.Boss()

        for key, value in data[i].items():
            setattr(boss, key, value)

        expected[boss.metric] = boss

    assert result == expected


def test_set_attrs(blank_class: t.Any) -> None:
    serializer = Serializer()

    data = {"test": 1, "other": "hello"}
    serializer._set_attrs(blank_class, data, "test", "other")  # type: ignore

    assert blank_class.test == 1
    assert blank_class.other == "hello"


def test_set_attrs_no_attrs(blank_class: t.Any) -> None:
    serializer = Serializer()

    data = {"test": 1, "other": "hello"}
    serializer._set_attrs(blank_class, data)  # type: ignore

    assert not hasattr(blank_class, "test")
    assert not hasattr(blank_class, "other")


def test_set_attrs_transform(blank_class: t.Any) -> None:
    serializer = Serializer()

    data = {"test": 1, "other": "hello"}
    serializer._set_attrs(  # type: ignore
        blank_class, data, "test", "other", transform=lambda a: a * 2
    )

    assert blank_class.test == 2
    assert blank_class.other == "hellohello"


def test_set_attrs_camel_case(blank_class: t.Any) -> None:
    serializer = Serializer()

    data = {"testThing": 1, "otherThing": "hello"}
    serializer._set_attrs(  # type: ignore
        blank_class, data, "test_thing", "other_thing", camel_case=True
    )

    assert blank_class.test_thing == 1
    assert blank_class.other_thing == "hello"


def test_set_attrs_transform_camel_case(blank_class: t.Any) -> None:
    serializer = Serializer()

    data = {"testThing": 1, "otherThing": "hello"}
    serializer._set_attrs(  # type: ignore
        blank_class, data, "test_thing", "other_thing", camel_case=True, transform=lambda a: a * 2
    )

    assert blank_class.test_thing == 2
    assert blank_class.other_thing == "hellohello"


@mock.patch("wom.serializer.Serializer._set_attrs")
def test_set_attrs_cased(set_attrs: mock.MagicMock, blank_class: t.Any) -> None:
    serializer = Serializer()
    serializer._set_attrs_cased(blank_class, {}, "test", "other")  # type: ignore

    set_attrs.assert_called_once_with(
        blank_class, {}, "test", "other", transform=None, camel_case=True
    )


@mock.patch("wom.serializer.Serializer._set_attrs")
def test_set_attrs_cased_no_attrs(set_attrs: mock.MagicMock, blank_class: t.Any) -> None:
    serializer = Serializer()
    serializer._set_attrs_cased(blank_class, {})  # type: ignore

    set_attrs.assert_called_once_with(blank_class, {}, transform=None, camel_case=True)


@mock.patch("wom.serializer.Serializer._set_attrs")
def test_set_attrs_cased_transform(set_attrs: mock.MagicMock, blank_class: t.Any) -> None:
    serializer = Serializer()
    transform: t.Callable[[t.Any], t.Any] | None = lambda i: i

    serializer._set_attrs_cased(  # type: ignore
        blank_class, {}, "test", "other", transform=transform
    )

    set_attrs.assert_called_once_with(
        blank_class, {}, "test", "other", transform=transform, camel_case=True  # type: ignore
    )


def test_determine_hiscores_entry_item_skill() -> None:
    serializer = Serializer()
    data = {
        "experience": 69420,
        "level": 46,
        "rank": 100000,
    }

    result = serializer._determine_hiscores_entry_item(data)  # type: ignore

    assert isinstance(result, models.GroupHiscoresSkillItem)
    assert result.experience == 69420
    assert result.level == 46
    assert result.rank == 100000


def test_determine_hiscores_entry_item_boss() -> None:
    serializer = Serializer()
    data = {
        "kills": 900,
        "rank": 72000,
    }

    result = serializer._determine_hiscores_entry_item(data)  # type: ignore

    assert isinstance(result, models.GroupHiscoresBossItem)
    assert result.rank == 72000
    assert result.kills == 900


def test_determine_hiscores_entry_item_activity() -> None:
    serializer = Serializer()
    data = {
        "score": 654321,
        "rank": 1000,
    }

    result = serializer._determine_hiscores_entry_item(data)  # type: ignore

    assert isinstance(result, models.GroupHiscoresActivityItem)
    assert result.rank == 1000
    assert result.score == 654321


def test_determine_hiscores_entry_item_computed() -> None:
    serializer = Serializer()
    data = {
        "value": 666,
        "rank": 222,
    }

    result = serializer._determine_hiscores_entry_item(data)  # type: ignore

    assert isinstance(result, models.GroupHiscoresComputedMetricItem)
    assert result.rank == 222
    assert result.value == 666


def test_determine_hiscores_entry_item_invalid() -> None:
    serializer = Serializer()
    data = {}

    with pytest.raises(ValueError) as e:
        serializer._determine_hiscores_entry_item(data)  # type: ignore

    assert e.exconly() == "ValueError: Unknown hiscores entry item: {}"


def test_deserialize_base_achievement() -> None:
    serializer = Serializer()
    model = models.Achievement()
    data = {
        "metric": "attack",
        "measure": "experience",
        "name": "lol",
        "playerId": 123,
        "threshold": 5,
        "accuracy": None,
    }

    serializer._deserialize_base_achievement(model, data)  # type: ignore

    assert model.metric is Skills.Attack
    assert model.measure is models.AchievementMeasure.Experience
    assert model.name == "lol"
    assert model.player_id == 123
    assert model.threshold == 5
    assert model.accuracy == None


def test_deserialize_player(
    player_dict: dict[str, t.Any], deserialized_player: models.Player
) -> None:
    serializer = Serializer()

    result = serializer.deserialize_player(player_dict)

    assert result == deserialized_player


def test_deserialize_player_details(
    player_detail_dict: dict[str, t.Any], deserialized_player_detail: models.PlayerDetail
) -> None:
    serializer = Serializer()

    result = serializer.deserialize_player_details(player_detail_dict)

    assert result == deserialized_player_detail


def test_deserialize_snapshot(
    snapshot_dict: dict[str, t.Any], deserialized_snapshot: models.Snapshot
) -> None:
    serializer = Serializer()

    result = serializer.deserialize_snapshot(snapshot_dict)

    assert result == deserialized_snapshot


def test_deserialize_snapshot_data(
    snapshot_data_dict: dict[str, t.Any], deserialized_snapshot_data: models.Snapshot
) -> None:
    serializer = Serializer()

    result = serializer.deserialize_snapshot_data(snapshot_data_dict)

    assert result == deserialized_snapshot_data


def test_deserialize_skill(skill_dict: dict[str, t.Any], deserialized_skill: models.Skill) -> None:
    serializer = Serializer()

    result = serializer.deserialize_skill(skill_dict)

    assert result == deserialized_skill


def test_deserialize_boss(boss_dict: dict[str, t.Any], deserialized_boss: models.Boss) -> None:
    serializer = Serializer()

    result = serializer.deserialize_boss(boss_dict)

    assert result == deserialized_boss


def test_deserialize_activity(
    activity_dict: dict[str, t.Any], deserialized_activity: models.Activity
) -> None:
    serializer = Serializer()

    result = serializer.deserialize_activity(activity_dict)

    assert result == deserialized_activity


def test_deserialize_computed_metric(
    computed_dict: dict[str, t.Any], deserialized_computed: models.ComputedMetric
) -> None:
    serializer = Serializer()

    result = serializer.deserialize_computed_metric(computed_dict)

    assert result == deserialized_computed


def test_deserialized_asserted_player_type(
    assert_player_type_dict: dict[str, t.Any],
    deserialized_assert_player_type: models.AssertPlayerType,
) -> None:
    serializer = Serializer()

    result = serializer.deserialize_asserted_player_type(assert_player_type_dict)

    assert result == deserialized_assert_player_type
