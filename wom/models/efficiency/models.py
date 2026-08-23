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

from wom import enums

from ..base import BaseModel

__all__ = (
    "BossMetaConfig",
    "SkillMetaBonus",
    "SkillMetaConfig",
    "SkillMetaMethod",
)


class SkillMetaMethod(BaseModel):
    """A training method used to compute a skill's efficient hours played."""

    rate: float
    """The experience per hour for this method."""

    start_exp: int
    """The experience at which this method begins."""

    description: str
    """A description of the training method."""

    real_rate: t.Optional[float] = None
    """The real experience per hour, if it differs from `rate`."""


class SkillMetaBonus(BaseModel):
    """A bonus experience relationship between two skills."""

    origin_skill: enums.Metric
    """The skill that produces the bonus experience."""

    bonus_skill: enums.Metric
    """The skill that receives the bonus experience."""

    start_exp: int
    """The experience at which the bonus begins."""

    end_exp: int
    """The experience at which the bonus ends."""

    end: bool
    """Whether this bonus applies at the end of training the origin skill."""

    ratio: float
    """The ratio of bonus experience gained."""

    max_bonus: t.Optional[float] = None
    """The maximum bonus experience that can be gained, if capped."""


class SkillMetaConfig(BaseModel):
    """The efficiency rate configuration for a particular skill."""

    skill: enums.Metric
    """The skill being configured."""

    methods: t.List[SkillMetaMethod]
    """The [`methods`][wom.SkillMetaMethod] used to train the skill."""

    bonuses: t.List[SkillMetaBonus]
    """The [`bonuses`][wom.SkillMetaBonus] applied while training the skill."""


class BossMetaConfig(BaseModel):
    """The efficiency rate configuration for a particular boss."""

    boss: enums.Metric
    """The boss being configured."""

    rate: float
    """The kills per hour for this boss."""
