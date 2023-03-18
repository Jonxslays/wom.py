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

from wom import BaseModel
from wom import GroupMemberFragment
from wom import GroupRole
from wom import Team


def test_base_to_dict() -> None:
    assert BaseModel().to_dict() == {}


def test_team_init() -> None:
    team = Team("woo", ["Jonxslays", "Zezima"])
    assert team.name == "woo"
    assert team.participants == ["Jonxslays", "Zezima"]
    assert team.to_dict() == {"name": "woo", "participants": ["Jonxslays", "Zezima"]}


def test_group_member_fragment_init() -> None:
    fragment = GroupMemberFragment("Jonxslays", GroupRole.Adept)
    assert fragment.username == "Jonxslays"
    assert fragment.role is GroupRole.Adept
    assert fragment.to_dict() == {"username": "Jonxslays", "role": GroupRole.Adept}
