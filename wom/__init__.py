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

"""All models, enums, services, etc are exported here in the main
wom module.

!!! tip

    Know what you're looking for? Hit the search bar ^!
"""

from __future__ import annotations

from typing import Final

__packagename__: Final[str] = "wom.py"
__version__: Final[str] = "2.0.2"
__author__: Final[str] = "Jonxslays"
__copyright__: Final[str] = "2023-present Jonxslays"
__description__: Final[str] = "An asynchronous wrapper for the Wise Old Man API."
__url__: Final[str] = "https://github.com/Jonxslays/wom.py"
__docs__: Final[str] = "https://jonxslays.github.io/wom.py"
__repository__: Final[str] = __url__
__license__: Final[str] = "MIT"
__git_sha__: Final[str] = "[HEAD]"

from . import client
from . import constants
from . import enums
from . import errors
from . import models
from . import result
from . import routes
from . import serializer
from . import services
from .client import *
from .enums import *
from .errors import *
from .models import *
from .result import *
from .routes import *
from .serializer import *
from .services import *

__all__ = (
    "client",
    "constants",
    "enums",
    "errors",
    "models",
    "result",
    "routes",
    "serializer",
    "services",
    "Achievement",
    "AchievementMeasure",
    "AchievementProgress",
    "Activities",
    "Activity",
    "ActivityGains",
    "ActivityLeader",
    "Archive",
    "BaseEnum",
    "BaseModel",
    "BaseService",
    "Boss",
    "Bosses",
    "BossGains",
    "BossLeader",
    "Client",
    "Country",
    "Competition",
    "CompetitionCSVTableType",
    "CompetitionDetail",
    "CompetitionHistoryDataPoint",
    "CompetitionParticipationDetail",
    "CompetitionParticipation",
    "CompetitionProgress",
    "CompetitionService",
    "CompetitionStatus",
    "CompetitionType",
    "CompiledRoute",
    "ComputedGains",
    "ComputedMetric",
    "ComputedMetricLeader",
    "ComputedMetrics",
    "CreatedCompetitionDetail",
    "CreatedGroupDetail",
    "DeltaLeaderboardEntry",
    "DeltaService",
    "EfficiencyService",
    "Err",
    "Gains",
    "Group",
    "GroupActivity",
    "GroupActivityType",
    "GroupDetail",
    "GroupHiscoresActivityItem",
    "GroupHiscoresBossItem",
    "GroupHiscoresComputedMetricItem",
    "GroupHiscoresEntry",
    "GroupHiscoresSkillItem",
    "GroupMemberFragment",
    "GroupMemberGains",
    "GroupMembership",
    "GroupRole",
    "GroupService",
    "GroupStatistics",
    "HttpErrorResponse",
    "HttpService",
    "HttpSuccessResponse",
    "Membership",
    "Metric",
    "MetricLeader",
    "MetricLeaders",
    "NameChange",
    "NameChangeReviewContext",
    "NameChangeReviewReason",
    "NameChangeService",
    "NameChangeStatus",
    "Ok",
    "Participation",
    "Period",
    "PlayerAchievementProgress",
    "PlayerArchive",
    "PlayerBuild",
    "PlayerCompetitionStanding",
    "PlayerGains",
    "PlayerGainsData",
    "PlayerMembership",
    "Player",
    "PlayerDetail",
    "PlayerParticipation",
    "PlayerService",
    "PlayerStatus",
    "PlayerType",
    "Record",
    "RecordService",
    "RecordLeaderboardEntry",
    "Result",
    "Route",
    "Serializer",
    "Skill",
    "SkillGains",
    "SkillLeader",
    "Skills",
    "SnapshotData",
    "Snapshot",
    "SnapshotTimelineEntry",
    "SocialLinks",
    "Team",
    "Top5ProgressResult",
    "UnwrapError",
    "WomError",
)
