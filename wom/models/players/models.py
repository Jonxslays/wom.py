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

from dataclasses import dataclass
from datetime import datetime

from wom import enums

from .enums import AchievementMeasure
from .enums import Country
from .enums import PlayerBuild
from .enums import PlayerType

__all__ = (
    "AchievementModel",
    "ActivityModel",
    "AssertPlayerTypeModel",
    "BossModel",
    "ComputedMetricModel",
    "PlayerAchievementProgressModel",
    "PlayerModel",
    "PlayerDetailModel",
    "SkillModel",
    "SnapshotDataModel",
    "SnapshotModel",
)


@dataclass(slots=True, init=False)
class SkillModel:
    metric: enums.Skill
    ehp: int
    rank: int
    level: int
    experience: int


@dataclass(slots=True, init=False)
class BossModel:
    metric: enums.Boss
    ehb: int
    rank: int
    kills: int


@dataclass(slots=True, init=False)
class ActivityModel:
    metric: enums.Activity
    rank: int
    score: int


@dataclass(slots=True, init=False)
class ComputedMetricModel:
    metric: enums.ComputedMetric
    rank: int
    value: int


@dataclass(slots=True, init=False)
class SnapshotDataModel:
    skills: list[SkillModel]
    bosses: list[BossModel]
    activities: list[ActivityModel]
    computed: list[ComputedMetricModel]


@dataclass(slots=True, init=False)
class SnapshotModel:
    id: int
    player_id: int
    created_at: datetime
    imported_at: datetime | None
    data: SnapshotDataModel


@dataclass(slots=True, init=False)
class PlayerModel:
    id: int
    username: str
    display_name: str
    type: PlayerType
    build: PlayerBuild
    country: Country | None
    flagged: bool
    exp: int
    ehp: float
    ehb: float
    ttm: float
    tt200m: float
    registered_at: datetime
    updated_at: datetime
    last_changed_at: datetime | None
    last_imported_at: datetime | None


@dataclass(slots=True, init=False)
class PlayerDetailModel:
    player: PlayerModel
    combat_level: int
    latest_snapshot: SnapshotModel | None


@dataclass(slots=True, init=False)
class AssertPlayerTypeModel:
    player: PlayerModel
    changed: bool


@dataclass(slots=True, init=False)
class AchievementModel:
    player_id: int
    name: str
    metric: enums.Metric
    measure: AchievementMeasure
    threshold: int
    created_at: datetime | None
    # TODO: This is only nullable on the progress model...


@dataclass(slots=True, init=False)
class PlayerAchievementProgressModel:
    achievement: AchievementModel
    current_value: int
    absolute_progress: float
    relative_progress: float
