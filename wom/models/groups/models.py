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

import attrs

from wom import enums

from ..base import BaseModel
from ..players import Gains
from ..players import Player
from ..players import Snapshot
from .enums import GroupRole

__all__ = (
    "ActivityLeader",
    "BossLeader",
    "ComputedMetricLeader",
    "Group",
    "GroupDetail",
    "GroupHiscoresActivityItem",
    "GroupHiscoresBossItem",
    "GroupHiscoresComputedMetricItem",
    "GroupHiscoresEntry",
    "GroupHiscoresSkillItem",
    "GroupMemberFragment",
    "GroupMemberGains",
    "GroupMembership",
    "GroupStatistics",
    "Membership",
    "MetricLeaders",
    "PlayerMembership",
    "SkillLeader",
)


@attrs.define(init=False)
class Group(BaseModel):
    """Represents a group of players on WOM."""

    id: int
    """The unique ID for this group."""

    name: str
    """The groups name."""

    clan_chat: str
    """The clan chat for this group."""

    description: t.Optional[str]
    """The groups optional description."""

    homeworld: t.Optional[int]
    """The groups optional homeworld."""

    verified: bool
    """Whether or not this group is verified."""

    score: int
    """The groups score."""

    created_at: datetime
    """The date the group was created."""

    updated_at: datetime
    """The date the group was updated."""

    member_count: int
    """The number of members in the group."""


@attrs.define(init=False)
class GroupDetail(BaseModel):
    """Represents details about a group."""

    group: Group
    """The [`Group`][wom.Group] itself."""

    memberships: t.List[GroupMembership]
    """A list of [`GroupMemberships`][wom.GroupMembership]."""

    verification_code: t.Optional[str]
    """The optional verification code for the group.

    !!! note

        This will only be present on group creation.
    """


@attrs.define(init=False)
class Membership(BaseModel):
    """Represents a membership in a group."""

    player_id: int
    """The unique ID of the player in this membership."""

    group_id: int
    """The group ID this membership belongs to."""

    role: t.Optional[GroupRole]
    """The optional [`GroupRole`][wom.GroupRole] for this membership."""

    created_at: datetime
    """The date this membership was created."""

    updated_at: datetime
    """The date this membership was updated."""


@attrs.define(init=False)
class GroupMembership(BaseModel):
    """Represents a group membership."""

    player: Player
    """The [`Player`][wom.Player] that is a member."""

    membership: Membership
    """The [`Membership`][wom.Membership] itself."""


@attrs.define(init=False)
class PlayerMembership(BaseModel):
    """Represents a player membership."""

    group: Group
    """The [`Group`][wom.Group] the player is a member of."""

    membership: Membership
    """The [`Membership`][wom.Membership] itself."""


@attrs.define
class GroupMemberFragment(BaseModel):
    """Represents a condensed group member.

    Args:
        username: The username of the group member.

        role: The optional [`GroupRole`][wom.models.GroupRole] to
            give the member.

    !!! tip

        This is a model class that you will create in order to send
        data to some endpoints.
    """

    def __init__(self, username: str, role: t.Optional[GroupRole] = None) -> None:
        self.username = username
        self.role = role

    username: str
    """The group members username."""

    role: t.Optional[GroupRole]
    """The optional [`GroupRole`][wom.GroupRole] for the member.
    """


@attrs.define(init=False)
class GroupHiscoresEntry(BaseModel):
    """Represents a group hiscores entry."""

    player: Player
    """The [`Player`][wom.Player] responsible for the entry."""

    data: t.Union[
        GroupHiscoresActivityItem,
        GroupHiscoresBossItem,
        GroupHiscoresSkillItem,
        GroupHiscoresComputedMetricItem,
    ]
    """The data for this hiscores entry."""


@attrs.define(init=False)
class GroupHiscoresSkillItem(BaseModel):
    """Represents a group hiscores item for skills."""

    rank: int
    """The rank of the hiscore."""

    level: int
    """The level of the skill."""

    experience: int
    """The experience in the skill."""


@attrs.define(init=False)
class GroupHiscoresBossItem(BaseModel):
    """Represents a group hiscores item for bosses."""

    rank: int
    """The rank of the hiscore."""

    kills: int
    """The number of boss kills."""


@attrs.define(init=False)
class GroupHiscoresActivityItem(BaseModel):
    """Represents a group hiscores item for activities."""

    rank: int
    """The rank of the hiscore."""

    score: int
    """The activity score."""


@attrs.define(init=False)
class GroupHiscoresComputedMetricItem(BaseModel):
    """Represents a group hiscores item for computed metrics."""

    rank: int
    """The rank of the hiscore."""

    value: int
    """The value of the computed metric."""


@attrs.define(init=False)
class SkillLeader(BaseModel):
    """Represents a leader in a particular skill."""

    metric: enums.Skills
    """The [`Skills`][wom.Skills] being measured."""

    rank: int
    """The players rank in the skill."""

    level: int
    """The players level in the skill."""

    experience: int
    """The players experience in the skill."""

    player: t.Optional[Player]
    """The player leading in this metric, or `None` if none do."""


@attrs.define(init=False)
class BossLeader(BaseModel):
    """Represents a leader in a particular boss."""

    metric: enums.Bosses
    """The [`Bosses`][wom.Bosses] being measured."""

    rank: int
    """The players rank in killing the boss."""

    kills: int
    """The number of kills the player has."""

    player: t.Optional[Player]
    """The player leading in this metric, or `None` if none do."""


@attrs.define(init=False)
class ActivityLeader(BaseModel):
    """Represents a leader in a particular activity."""

    metric: enums.Activities
    """The [`Activities`][wom.Activities] being measured."""

    rank: int
    """The players rank in the activity."""

    score: int
    """The players score in the activity."""

    player: t.Optional[Player]
    """The player leading in this metric, or `None` if none do."""


@attrs.define(init=False)
class ComputedMetricLeader(BaseModel):
    """Represents a leader in a particular computed metric."""

    metric: enums.ComputedMetrics
    """The [`ComputedMetrics`][wom.ComputedMetrics] being
    measured.
    """

    rank: int
    """The players rank in the computed metric."""

    value: int
    """The value of the computed metric."""

    player: t.Optional[Player]
    """The player leading in this metric, or `None` if none do."""


@attrs.define(init=False)
class MetricLeaders(BaseModel):
    """The leaders for each metric in a group."""

    skills: t.Dict[enums.Skills, SkillLeader]
    """A mapping of [`Skills`][wom.Skills] keys to [`SkillLeader`]
    [wom.SkillLeader] values.
    """

    bosses: t.Dict[enums.Bosses, BossLeader]
    """A mapping of [`Bosses`][wom.Bosses] keys to [`BossLeader`]
    [wom.BossLeader] values.
    """

    activities: t.Dict[enums.Activities, ActivityLeader]
    """A mapping of [`Activities`][wom.Activities] keys to [`ActivityLeader`]
    [wom.ActivityLeader] values.
    """

    computed: t.Dict[enums.ComputedMetrics, ComputedMetricLeader]
    """A mapping of [`ComputedMetrics`][wom.ComputedMetrics] keys to
    [`ComputedMetricLeader`][wom.ComputedMetricLeader] values.
    """


@attrs.define(init=False)
class GroupStatistics(BaseModel):
    """Represents accumulated group statistics."""

    maxed_combat_count: int
    """The number of maxed combat players in the group."""

    maxed_total_count: int
    """The number of maxed total level players in the group."""

    maxed_200ms_count: int
    """The number of maxed 200M xp players in the group."""

    average_stats: Snapshot
    """The average group statistics in a [`Snapshot`][wom.Snapshot]."""

    metric_leaders: MetricLeaders
    """The [`MetricLeaders`][wom.MetricLeaders] in this group for each
    metric.
    """


@attrs.define(init=False)
class GroupMemberGains(BaseModel):
    """Represents a leaderboard entry over the given delta."""

    start_date: datetime
    """The start date of the gains."""

    end_date: datetime
    """The end date of the gains."""

    player: Player
    """The [`Player`][wom.Player] that attained these gains."""

    data: Gains
    """The [`Gains`][wom.Gains] for this group member."""
