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

"""This module contains the models used to represent data returned
by the WOM API.

Enums related to specific services are also housed in the module.

!!! tip

    Most of the models here you won't create, but a few you will. Those
    will be documented as such.
"""

from __future__ import annotations

__all__ = (
    "Achievement",
    "AchievementMeasure",
    "AchievementProgress",
    "Activity",
    "ActivityGains",
    "ActivityLeader",
    "Archive",
    "BaseModel",
    "Boss",
    "BossGains",
    "BossLeader",
    "Country",
    "Competition",
    "CompetitionCSVTableType",
    "CompetitionDetail",
    "CompetitionHistoryDataPoint",
    "CompetitionParticipationDetail",
    "CompetitionParticipation",
    "CompetitionProgress",
    "CompetitionStatus",
    "CompetitionType",
    "ComputedGains",
    "ComputedMetric",
    "ComputedMetricLeader",
    "CreatedCompetitionDetail",
    "CreatedGroupDetail",
    "DeltaLeaderboardEntry",
    "Gains",
    "GroupDetail",
    "Group",
    "GroupActivity",
    "GroupActivityType",
    "GroupHiscoresActivityItem",
    "GroupHiscoresBossItem",
    "GroupHiscoresComputedMetricItem",
    "GroupHiscoresEntry",
    "GroupHiscoresSkillItem",
    "GroupMemberFragment",
    "GroupMemberGains",
    "GroupMembership",
    "GroupRole",
    "GroupStatistics",
    "HttpErrorResponse",
    "HttpSuccessResponse",
    "Membership",
    "MetricLeader",
    "MetricLeaders",
    "NameChange",
    "NameChangeReviewContext",
    "NameChangeReviewReason",
    "NameChangeStatus",
    "Participation",
    "PlayerAchievementProgress",
    "PlayerArchive",
    "PlayerBuild",
    "PlayerCompetitionStanding",
    "PlayerMembership",
    "Player",
    "PlayerDetail",
    "PlayerGains",
    "PlayerGainsData",
    "PlayerParticipation",
    "PlayerStatus",
    "PlayerType",
    "Record",
    "RecordLeaderboardEntry",
    "Skill",
    "SkillGains",
    "SkillLeader",
    "SnapshotData",
    "Snapshot",
    "SnapshotTimelineEntry",
    "SocialLinks",
    "Team",
    "Top5ProgressResult",
)

from .base import *
from .competitions import *
from .deltas import *
from .groups import *
from .http import *
from .names import *
from .players import *
from .records import *
