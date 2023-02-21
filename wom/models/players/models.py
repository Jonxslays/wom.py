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
    "Achievement",
    "AchievementProgress",
    "ActivityGains",
    "Activity",
    "AssertPlayerType",
    "BaseAchievement",
    "BaseSnapshot",
    "BossGains",
    "Boss",
    "ComputedGains",
    "ComputedMetric",
    "Gains",
    "PlayerAchievementProgress",
    "PlayerGainsData",
    "PlayerGains",
    "Player",
    "PlayerDetail",
    "StatisticsSnapshot",
    "SkillGains",
    "Skill",
    "SnapshotData",
    "Snapshot",
)


@dataclass(init=False)
class Skill(BaseModel):
    metric: enums.Skill
    rank: int
    level: int
    experience: int
    ehp: int


@dataclass(init=False)
class Boss(BaseModel):
    metric: enums.Boss
    rank: int
    kills: int
    ehb: int


@dataclass(init=False)
class Activity(BaseModel):
    metric: enums.Activity
    rank: int
    score: int


@dataclass(init=False)
class ComputedMetric(BaseModel):
    metric: enums.ComputedMetric
    rank: int
    value: int


@dataclass(init=False)
class SnapshotData(BaseModel):
    """The data associated with this snapshot."""

    skills: list[Skill]
    bosses: list[Boss]
    activities: list[Activity]
    computed: list[ComputedMetric]


@dataclass(init=False)
class BaseSnapshot(BaseModel):
    """The base snapshot other snapshots inherit from."""

    id: int
    """The unique ID of the snapshot."""
    player_id: int
    """The unique ID of the player for this snapshot."""
    imported_at: datetime | None
    """The date the snapshot was imported, if it was."""
    data: SnapshotData
    """The [`SnapshotData`][wom.models.SnapshotData] for the snapshot."""


@dataclass(init=False)
class Snapshot(BaseSnapshot):
    """Represents a player snapshot."""

    created_at: datetime
    """The date the snapshot was created."""


@dataclass(init=False)
class StatisticsSnapshot(BaseSnapshot):
    """Represents a player statistics snapshot."""

    created_at: datetime | None
    """The optional date the statistics snapshot was created."""


@dataclass(init=False)
class Player(BaseModel):
    """Represents a player on WOM."""

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


@dataclass(init=False)
class PlayerDetail(BaseModel):
    player: Player
    combat_level: int
    latest_snapshot: Snapshot | None


@dataclass(init=False)
class AssertPlayerType(BaseModel):
    player: Player
    changed: bool


@dataclass(init=False)
class BaseAchievement(BaseModel):
    player_id: int
    name: str
    metric: enums.Metric
    measure: AchievementMeasure
    threshold: int


@dataclass(init=False)
class Achievement(BaseAchievement):
    created_at: datetime


@dataclass(init=False)
class AchievementProgress(BaseAchievement):
    created_at: datetime | None


@dataclass(init=False)
class PlayerAchievementProgress(BaseModel):
    achievement: AchievementProgress
    current_value: int
    absolute_progress: float
    relative_progress: float


@dataclass(init=False)
class Gains(BaseModel):
    gained: float
    start: float
    end: float


@dataclass(init=False)
class SkillGains(BaseModel):
    metric: enums.Skill
    experience: Gains
    ehp: Gains
    rank: Gains
    level: Gains


@dataclass(init=False)
class BossGains(BaseModel):
    metric: enums.Boss
    ehb: Gains
    rank: Gains
    kills: Gains


@dataclass(init=False)
class ActivityGains(BaseModel):
    metric: enums.Activity
    rank: Gains
    score: Gains


@dataclass(init=False)
class ComputedGains(BaseModel):
    metric: enums.ComputedMetric
    rank: Gains
    value: Gains


@dataclass(init=False)
class PlayerGainsData(BaseModel):
    skills: list[SkillGains]
    bosses: list[BossGains]
    activities: list[ActivityGains]
    computed: list[ComputedGains]


@dataclass(init=False)
class PlayerGains(BaseModel):
    starts_at: datetime
    ends_at: datetime
    data: PlayerGainsData
