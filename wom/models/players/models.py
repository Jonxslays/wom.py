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

from datetime import datetime

import attrs

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


@attrs.define(init=False)
class Skill(BaseModel):
    """Details regarding a particular skill."""

    metric: enums.Skills
    """The [`Skills`][wom.enums.Skills] being measured."""

    rank: int
    """The players rank in the skill."""

    level: int
    """The players level in the skill."""

    experience: int
    """The players experience in the skill."""

    ehp: int
    """The players efficient hours played for the skill."""


@attrs.define(init=False)
class Boss(BaseModel):
    """Details regarding a particular boss."""

    metric: enums.Bosses
    """The [`Bosses`][wom.enums.Bosses] being measured."""

    rank: int
    """The players rank in killing the boss."""

    kills: int
    """The number of kills the player has."""

    ehb: int
    """The players efficient hours bossed for the boss."""


@attrs.define(init=False)
class Activity(BaseModel):
    """Details regarding a particular activity."""

    metric: enums.Activities
    """The [`Activities`][wom.enums.Activities] being measured."""

    rank: int
    """The players rank in the activity."""

    score: int
    """The players score in the activity."""


@attrs.define(init=False)
class ComputedMetric(BaseModel):
    """Details regarding a computed metric."""

    metric: enums.ComputedMetrics
    """The [`ComputedMetrics`][wom.enums.ComputedMetrics] being
    measured.
    """

    rank: int
    """The players rank in the computed metric."""

    value: int
    """The value of the computed metric."""


@attrs.define(init=False)
class SnapshotData(BaseModel):
    """The data associated with this snapshot."""

    skills: list[Skill]
    """A list of all [`Skills`][wom.models.Skill] stored in this
    snapshot.
    """

    bosses: list[Boss]
    """A list of all [`Bosses`][wom.models.Boss] stored in this
    snapshot.
    """

    activities: list[Activity]
    """A list of all [`Activities`][wom.models.Activity] stored in this
    snapshot.
    """

    computed: list[ComputedMetric]
    """A list of all [`ComputedMetrics`][wom.models.ComputedMetric]
    stored in this snapshot.
    """


@attrs.define(init=False)
class Snapshot(BaseModel):
    """Represents a player snapshot."""

    id: int
    """The unique ID of the snapshot."""

    player_id: int
    """The unique ID of the player for this snapshot."""

    imported_at: datetime | None
    """The date the snapshot was imported, if it was."""

    data: SnapshotData
    """The [`SnapshotData`][wom.models.SnapshotData] for the
    snapshot.
    """

    created_at: datetime
    """The date the snapshot was created."""


@attrs.define(init=False)
class StatisticsSnapshot(BaseModel):
    """Represents a player statistics snapshot."""

    id: int
    """The unique ID of the snapshot."""

    player_id: int
    """The unique ID of the player for this snapshot."""

    imported_at: datetime | None
    """The date the snapshot was imported, if it was."""

    data: SnapshotData
    """The [`SnapshotData`][wom.models.SnapshotData] for the
    snapshot.
    """

    created_at: datetime | None
    """The optional date the statistics snapshot was created."""


@attrs.define(init=False)
class Player(BaseModel):
    """Represents a player on WOM."""

    id: int
    """The players unique ID."""

    username: str
    """The players username, always lowercase and 1-12 chars."""

    display_name: str
    """The players display name, supports capitalization ."""

    type: PlayerType
    """The [`PlayerType`][wom.models.PlayerType] for this player."""

    build: PlayerBuild
    """The [`PlayerBuild`][wom.models.PlayerBuild] for this player."""

    country: Country | None
    """The players [`Country`][wom.models.Country] country of origin, if
    they have one set.
    """

    flagged: bool
    """Whether the player is flagged for having an invalid snapshot
    history.
    """

    exp: int
    """The players overall experience."""

    ehp: float
    """The players efficient hours played."""

    ehb: float
    """The players efficient hours bossed."""

    ttm: float
    """The players time to max, in hours."""

    tt200m: float
    """The players time to 200m xp all skills, in hours."""

    registered_at: datetime
    """The date the player was registered with WOM."""

    updated_at: datetime
    """The date the player was last updated with WOM."""

    last_changed_at: datetime | None
    """The date of the players last change (xp gain, boss kc, etc)."""

    last_imported_at: datetime | None
    """The date of the last player history import."""


@attrs.define(init=False)
class PlayerDetail(BaseModel):
    """Represents details about a player."""

    player: Player
    """The [Player][wom.models.Player]."""

    combat_level: int
    """The players combat level."""

    latest_snapshot: Snapshot | None
    """The latest snapshot for the player, if there is one."""


@attrs.define(init=False)
class AssertPlayerType(BaseModel):
    """Represents a player type that has been asserted."""

    player: Player
    """The player who's type was asserted."""

    changed: bool
    """Whether or not the player type changed."""


@attrs.define(init=False)
class Achievement(BaseModel):
    """Represents an achievement made by a player."""

    player_id: int
    """The unique ID of the player."""

    name: str
    """The name of the achievement."""

    metric: enums.Metric
    """The [`Metric`][wom.enums.Metric] for this achievement."""

    measure: AchievementMeasure
    """The [`AchievementMeasure`][wom.models.AchievementMeasure] that
    the player obtained.
    """

    threshold: int
    """The threshold for this achievement."""

    created_at: datetime
    """The date the achievement was achieved."""

    accuracy: int | None
    """The margin of error for the achievements creation date.

    !!! note

        Can be `None` if the achievement hasn't been recalculated since
        the addition of this field (~ Feb 2023). It can also be -1 for
        achievements with unknown dates.
    """


@attrs.define(init=False)
class AchievementProgress(BaseModel):
    """Represents progress made toward an achievement."""

    player_id: int
    """The unique ID of the player."""

    name: str
    """The name of the achievement."""

    metric: enums.Metric
    """The [`Metric`][wom.enums.Metric] for this achievement."""

    measure: AchievementMeasure
    """The [`AchievementMeasure`][wom.models.AchievementMeasure] that
    the player obtained.
    """

    threshold: int
    """The threshold for this achievement."""

    created_at: datetime | None
    """The date the achievement was achieved, or `None` if it has not
    been achieved.
    """

    accuracy: int | None
    """The margin of error for the achievements creation date.

    !!! note

        Can be `None` if the achievement hasn't been recalculated since
        the addition of this field (~ Feb 2023). It can also be -1 for
        achievements with unknown dates.
    """


@attrs.define(init=False)
class PlayerAchievementProgress(BaseModel):
    """Represents a players progress toward an achievement."""

    achievement: AchievementProgress
    """The [AchievementProgress][wom.models.AchievementProgress]
    made.
    """

    current_value: int
    """The current value for the achievement's metric."""

    absolute_progress: float
    """The players current absolute progress toward the achievement.

    Scale of 0-1 with 1 being 100% progress.
    """

    relative_progress: float
    """The players current relative progress toward the achievement
    starting from the previous achievement.

    Scale of 0-1 with 1 being 100% progress.
    """


@attrs.define(init=False)
class Gains(BaseModel):
    """Represents gains made by a player."""

    gained: float
    """The amount gained."""

    start: float
    """The starting amount."""

    end: float
    """The ending amount."""


@attrs.define(init=False)
class SkillGains(BaseModel):
    """Represents skill gains made by a player."""

    metric: enums.Skills
    """The [`Skills`][wom.enums.Skills] being measured."""

    experience: Gains
    """The experience [`Gains`][wom.models.Gains]."""

    ehp: Gains
    """The efficient hours played [`Gains`][wom.models.Gains]."""

    rank: Gains
    """The rank [`Gains`][wom.models.Gains]."""

    level: Gains
    """The level [`Gains`][wom.models.Gains]."""


@attrs.define(init=False)
class BossGains(BaseModel):
    metric: enums.Bosses
    """The [`Bosses`][wom.enums.Bosses] being measured."""

    ehb: Gains
    """The efficient hours bossed [`Gains`][wom.models.Gains]."""

    rank: Gains
    """The rank [`Gains`][wom.models.Gains]."""

    kills: Gains
    """The boss kill [`Gains`][wom.models.Gains]."""


@attrs.define(init=False)
class ActivityGains(BaseModel):
    metric: enums.Activities
    """The [`Activities`][wom.enums.Activities] being measured."""

    rank: Gains
    """The rank [`Gains`][wom.models.Gains]."""

    score: Gains
    """The score [`Gains`][wom.models.Gains]."""


@attrs.define(init=False)
class ComputedGains(BaseModel):
    metric: enums.ComputedMetrics
    """The [`ComputedMetrics`][wom.enums.ComputedMetrics] being
    measured.
    """

    rank: Gains
    """The rank [`Gains`][wom.models.Gains]."""

    value: Gains
    """The value [`Gains`][wom.models.Gains]."""


@attrs.define(init=False)
class PlayerGainsData(BaseModel):
    """Contains all the player gains data."""

    skills: list[SkillGains]
    """A list of all [`SkillGains`][wom.models.SkillGains]."""

    bosses: list[BossGains]
    """A list of all [`BossGains`][wom.models.BossGains]."""

    activities: list[ActivityGains]
    """A list of all [`ActivityGains`][wom.models.ActivityGains]."""

    computed: list[ComputedGains]
    """A list of all [`ComputedGains`][wom.models.ComputedGains]."""


@attrs.define(init=False)
class PlayerGains(BaseModel):
    """Gains made by a player."""

    starts_at: datetime
    """The date the gains started at."""

    ends_at: datetime
    """The date the gains ended at."""

    data: PlayerGainsData
    """The [`PlayerGainsData`][wom.models.PlayerGainsData] for the
    player.
    """
