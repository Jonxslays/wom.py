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

from ..base import BaseModel
from .enums import AchievementMeasure
from .enums import Country
from .enums import PlayerBuild
from .enums import PlayerType

__all__ = (
    "AchievementModel",
    "AchievementProgressModel",
    "ActivityGainsModel",
    "ActivityModel",
    "AssertPlayerTypeModel",
    "BaseAchievementModel",
    "BossGainsModel",
    "BossModel",
    "ComputedGainsModel",
    "ComputedMetricModel",
    "GainsModel",
    "PlayerAchievementProgressModel",
    "PlayerGainsDataModel",
    "PlayerGainsModel",
    "PlayerModel",
    "PlayerDetailModel",
    "SkillGainsModel",
    "SkillModel",
    "SnapshotDataModel",
    "SnapshotModel",
)


@dataclass(slots=True, init=False)
class SkillModel(BaseModel):
    metric: enums.Skill
    rank: int
    level: int
    experience: int
    ehp: int


@dataclass(slots=True, init=False)
class BossModel(BaseModel):
    metric: enums.Boss
    rank: int
    kills: int
    ehb: int


@dataclass(slots=True, init=False)
class ActivityModel(BaseModel):
    metric: enums.Activity
    rank: int
    score: int


@dataclass(slots=True, init=False)
class ComputedMetricModel(BaseModel):
    metric: enums.ComputedMetric
    rank: int
    value: int


@dataclass(slots=True, init=False)
class SnapshotDataModel(BaseModel):
    skills: list[SkillModel]
    bosses: list[BossModel]
    activities: list[ActivityModel]
    computed: list[ComputedMetricModel]


@dataclass(slots=True, init=False)
class SnapshotModel(BaseModel):
    id: int
    player_id: int
    created_at: datetime
    imported_at: datetime | None
    data: SnapshotDataModel


@dataclass(slots=True, init=False)
class PlayerModel(BaseModel):
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
class PlayerDetailModel(BaseModel):
    player: PlayerModel
    combat_level: int
    latest_snapshot: SnapshotModel | None


@dataclass(slots=True, init=False)
class AssertPlayerTypeModel(BaseModel):
    player: PlayerModel
    changed: bool


@dataclass(slots=True, init=False)
class BaseAchievementModel(BaseModel):
    player_id: int
    name: str
    metric: enums.Metric
    measure: AchievementMeasure
    threshold: int


@dataclass(slots=True, init=False)
class AchievementModel(BaseAchievementModel):
    created_at: datetime


@dataclass(slots=True, init=False)
class AchievementProgressModel(BaseAchievementModel):
    created_at: datetime | None


@dataclass(slots=True, init=False)
class PlayerAchievementProgressModel(BaseModel):
    achievement: AchievementProgressModel
    current_value: int
    absolute_progress: float
    relative_progress: float


@dataclass(slots=True, init=False)
class GainsModel(BaseModel):
    gained: float
    start: float
    end: float


@dataclass(slots=True, init=False)
class SkillGainsModel(BaseModel):
    metric: enums.Skill
    experience: GainsModel
    ehp: GainsModel
    rank: GainsModel
    level: GainsModel


@dataclass(slots=True, init=False)
class BossGainsModel(BaseModel):
    metric: enums.Boss
    ehb: GainsModel
    rank: GainsModel
    kills: GainsModel


@dataclass(slots=True, init=False)
class ActivityGainsModel(BaseModel):
    metric: enums.Activity
    rank: GainsModel
    score: GainsModel


@dataclass(slots=True, init=False)
class ComputedGainsModel(BaseModel):
    metric: enums.ComputedMetric
    rank: GainsModel
    value: GainsModel


@dataclass(slots=True, init=False)
class PlayerGainsDataModel(BaseModel):
    skills: list[SkillGainsModel]
    bosses: list[BossGainsModel]
    activities: list[ActivityGainsModel]
    computed: list[ComputedGainsModel]


@dataclass(slots=True, init=False)
class PlayerGainsModel(BaseModel):
    starts_at: datetime
    ends_at: datetime
    data: PlayerGainsDataModel
