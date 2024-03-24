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

"""Competition related enums."""

from __future__ import annotations

from wom.enums import BaseEnum

__all__ = ("CompetitionCSVTableType", "CompetitionStatus", "CompetitionType")


class CompetitionType(BaseEnum):
    """Competition types available on WOM."""

    Classic = "classic"
    Team = "team"


class CompetitionStatus(BaseEnum):
    """Potential competition statuses."""

    Upcoming = "upcoming"
    Ongoing = "ongoing"
    Finished = "finished"


class CompetitionCSVTableType(BaseEnum):
    """Table types used to return competition CSV details."""

    Participants = "participants"
    Team = "team"
    Teams = "teams"
