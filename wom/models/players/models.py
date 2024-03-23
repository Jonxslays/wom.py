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

from wom import enums

from ..base import BaseModel
from .enums import AchievementMeasure
from .enums import Country
from .enums import PlayerBuild
from .enums import PlayerStatus
from .enums import PlayerType

__all__ = (
    "Achievement",
    "AchievementProgress",
    "ActivityGains",
    "Activity",
    "Archive",
    "AssertPlayerType",
    "BossGains",
    "Boss",
    "ComputedGains",
    "ComputedMetric",
    "Gains",
    "PlayerAchievementProgress",
    "PlayerArchive",
    "PlayerGainsData",
    "PlayerGains",
    "Player",
    "PlayerDetail",
    "SkillGains",
    "Skill",
    "SnapshotData",
    "Snapshot",
    "SnapshotTimelineEntry",
)


class Skill(BaseModel):
    """Details regarding a particular skill."""

    metric: enums.Metric
    """The skill being measured."""

    rank: int
    """The players rank in the skill."""

    level: int
    """The players level in the skill."""

    experience: int
    """The players experience in the skill."""

    ehp: float
    """The players efficient hours played for the skill."""


class Boss(BaseModel):
    """Details regarding a particular boss."""

    metric: enums.Metric
    """The boss being measured."""

    rank: int
    """The players rank in killing the boss."""

    kills: int
    """The number of kills the player has."""

    ehb: float
    """The players efficient hours bossed for the boss."""


class Activity(BaseModel):
    """Details regarding a particular activity."""

    metric: enums.Metric
    """The activity being measured."""

    rank: int
    """The players rank in the activity."""

    score: int
    """The players score in the activity."""


class ComputedMetric(BaseModel):
    """Details regarding a computed metric."""

    metric: enums.Metric
    """The computed metric being measured."""

    rank: int
    """The players rank in the computed metric."""

    value: float
    """The value of the computed metric."""


class SnapshotData(BaseModel):
    """The data associated with this snapshot."""

    skills: t.Dict[enums.Metric, Skill]
    """A mapping of skill keys to skill values from this snapshot."""

    bosses: t.Dict[enums.Metric, Boss]
    """A mapping of boss keys to boss values from this snapshot."""

    activities: t.Dict[enums.Metric, Activity]
    """A mapping of activity keys to activity values from this snapshot."""

    computed: t.Dict[enums.Metric, ComputedMetric]
    """A mapping of computed metric keys to computed metric values from
    this snapshot.
    """


class Snapshot(BaseModel):
    """Represents a player snapshot."""

    id: int
    """The unique ID of the snapshot."""

    player_id: int
    """The unique ID of the player for this snapshot."""

    imported_at: t.Optional[datetime]
    """The date the snapshot was imported, if it was."""

    data: SnapshotData
    """The [`SnapshotData`][wom.SnapshotData] for the snapshot."""

    created_at: datetime
    """The date the snapshot was created."""


class Player(BaseModel):
    """Represents a player on WOM."""

    id: int
    """The players unique ID."""

    username: str
    """The players username, always lowercase and 1-12 chars."""

    display_name: str
    """The players display name, supports capitalization ."""

    type: PlayerType
    """The [`PlayerType`][wom.PlayerType] for this player."""

    build: PlayerBuild
    """The [`PlayerBuild`][wom.PlayerBuild] for this player."""

    country: t.Optional[Country]
    """The players [`Country`][wom.Country] country of origin, if they
    have one set.
    """

    status: PlayerStatus
    """The players status, i.e. flagged, archived, etc."""

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

    updated_at: t.Optional[datetime]
    """The date the player was last successfully updated with WOM."""

    last_changed_at: t.Optional[datetime]
    """The date of the players last change (xp gain, boss kc, etc)."""

    last_imported_at: t.Optional[datetime]
    """The date of the last player history import."""


class PlayerDetail(Player):
    """Represents details about a player."""

    combat_level: int
    """The players combat level."""

    latest_snapshot: t.Optional[Snapshot]
    """The latest snapshot for the player, if there is one."""

    archive: t.Optional[Archive] = None
    """The players archive information, if any."""


class AssertPlayerType(BaseModel):
    """Represents a player type that has been asserted."""

    player: Player
    """The player who's type was asserted."""

    changed: bool
    """Whether or not the player type changed."""


class Achievement(BaseModel):
    """Represents an achievement made by a player."""

    player_id: int
    """The unique ID of the player."""

    name: str
    """The name of the achievement."""

    metric: enums.Metric
    """The [`Metric`][wom.Metric] for this achievement."""

    measure: AchievementMeasure
    """The [`AchievementMeasure`][wom.AchievementMeasure] that
    the player obtained.
    """

    threshold: int
    """The threshold for this achievement."""

    created_at: datetime
    """The date the achievement was achieved."""

    accuracy: t.Optional[int]
    """The margin of error for the achievements creation date.

    !!! note

        Can be `None` if the achievement hasn't been recalculated since
        the addition of this field (~ Feb 2023). It can also be -1 for
        achievements with unknown dates.
    """


class AchievementProgress(BaseModel):
    """Represents progress made toward an achievement."""

    player_id: int
    """The unique ID of the player."""

    name: str
    """The name of the achievement."""

    metric: enums.Metric
    """The [`Metric`][wom.Metric] for this achievement."""

    measure: AchievementMeasure
    """The [`AchievementMeasure`][wom.AchievementMeasure] that
    the player obtained.
    """

    threshold: int
    """The threshold for this achievement."""

    created_at: t.Optional[datetime]
    """The date the achievement was achieved, or `None` if it has not
    been achieved.
    """

    accuracy: t.Optional[int]
    """The margin of error for the achievements creation date.

    !!! note

        Can be `None` if the achievement hasn't been recalculated since
        the addition of this field (~ Feb 2023). It can also be -1 for
        achievements with unknown dates.
    """


class PlayerAchievementProgress(AchievementProgress):
    """Represents a players progress toward an achievement."""

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


class Gains(BaseModel):
    """Represents gains made by a player."""

    gained: float
    """The amount gained."""

    start: float
    """The starting amount."""

    end: float
    """The ending amount."""


class SkillGains(BaseModel):
    """Represents skill gains made by a player."""

    metric: enums.Metric
    """The skill being measured."""

    experience: Gains
    """The experience [`Gains`][wom.Gains]."""

    ehp: Gains
    """The efficient hours played [`Gains`][wom.Gains]."""

    rank: Gains
    """The rank [`Gains`][wom.Gains]."""

    level: Gains
    """The level [`Gains`][wom.Gains]."""


class BossGains(BaseModel):
    """Represents boss gains made by a player."""

    metric: enums.Metric
    """The boss being measured."""

    ehb: Gains
    """The efficient hours bossed [`Gains`][wom.Gains]."""

    rank: Gains
    """The rank [`Gains`][wom.Gains]."""

    kills: Gains
    """The boss kill [`Gains`][wom.Gains]."""


class ActivityGains(BaseModel):
    """Represents activity gains made by a player."""

    metric: enums.Metric
    """The activity being measured."""

    rank: Gains
    """The rank [`Gains`][wom.Gains]."""

    score: Gains
    """The score [`Gains`][wom.Gains]."""


class ComputedGains(BaseModel):
    """Represents computed gains made by a player."""

    metric: enums.Metric
    """The computed metric being measured."""

    rank: Gains
    """The rank [`Gains`][wom.Gains]."""

    value: Gains
    """The value [`Gains`][wom.Gains]."""


class PlayerGainsData(BaseModel):
    """Contains all the player gains data."""

    skills: t.Dict[enums.Metric, SkillGains]
    """A mapping of skill keys to [`SkillGains`] [wom.SkillGains] values."""

    bosses: t.Dict[enums.Metric, BossGains]
    """A mapping of boss keys to [`BossGains`][wom.BossGains] values."""

    activities: t.Dict[enums.Metric, ActivityGains]
    """A mapping of activity keys to [`ActivityGains`][wom.ActivityGains]
    values.
    """

    computed: t.Dict[enums.Metric, ComputedGains]
    """A mapping of computed metric keys to [`ComputedGains`]
    [wom.ComputedGains] values.
    """


class PlayerGains(BaseModel):
    """Gains made by a player."""

    starts_at: datetime
    """The date the gains started at."""

    ends_at: datetime
    """The date the gains ended at."""

    data: PlayerGainsData
    """The [`PlayerGainsData`][wom.PlayerGainsData] for the player."""


class SnapshotTimelineEntry(BaseModel):
    """An entry representing a point in time of a players gains."""

    value: int
    """The players value for a specific metric, at a specific point in
    time."""

    rank: int
    """The players rank for a specific metric, at a specific point in
    time."""

    date: datetime
    """The date this timeline entry was recorded."""


class Archive(BaseModel):
    """Information detailing a player that has been archived."""

    player_id: int
    """The ID of the parent player that was archived."""

    previous_username: str
    """The players previous username before the archive."""

    archive_username: str
    """The players placeholder username after the archive."""

    restored_username: t.Optional[str]
    """The players new username after restoration from archive. Can be
    `None` if the player has not been restored."""

    created_at: datetime
    """The date the archive was created."""

    restored_at: t.Optional[datetime]
    """The date the player was restored, if they have been."""


class PlayerArchive(Archive):
    """Information detailing a player that has been archived, including the
    [`Player`][wom.Player] object."""

    player: Player
    """The player information."""
