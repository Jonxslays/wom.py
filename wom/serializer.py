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
from wom import models

__all__ = ("Serializer",)


class Serializer:
    __slots__ = ()

    def _to_js_casing(self, value: str) -> str:
        if "_" not in value:
            return value

        values = value.split("_")

        for i, v in enumerate(values[1:]):
            values[i + 1] = v.title()

        return "".join(values)

    def _dt_from_iso(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.rstrip("Z"))

    def _dt_from_iso_maybe(self, timestamp: str | None) -> datetime | None:
        return self._dt_from_iso(timestamp) if timestamp else None

    def _set_attrs_with_js_casing(
        self, model: t.Any, data: dict[str, t.Any], *normalized_attrs: str
    ) -> None:
        for attr in normalized_attrs:
            setattr(model, attr, data[self._to_js_casing(attr)])

    def deserialize_player(self, data: dict[str, t.Any]) -> models.PlayerModel:
        player = models.PlayerModel()
        self._set_attrs_with_js_casing(
            player,
            data,
            "id",
            "username",
            "display_name",
            "flagged",
            "exp",
            "ehp",
            "ehb",
            "ttm",
            "tt200m",
        )

        player.type = models.PlayerType.from_str(data["type"])
        player.build = models.PlayerBuild.from_str(data["build"])
        player.country = models.Country.from_str_maybe(data["country"])
        player.registered_at = self._dt_from_iso(data["registeredAt"])
        player.updated_at = self._dt_from_iso(data["registeredAt"])
        player.last_changed_at = self._dt_from_iso_maybe(data["lastChangedAt"])
        player.last_imported_at = self._dt_from_iso_maybe(data["lastImportedAt"])
        return player

    def deserialize_player_details(self, data: dict[str, t.Any]) -> models.PlayerDetailModel:
        details = models.PlayerDetailModel()
        details.combat_level = data["combatLevel"]
        details.player = self.deserialize_player(data)
        details.latest_snapshot = self.deserialize_snapshot(data["latestSnapshot"])
        return details

    def deserialize_snapshot(self, data: dict[str, t.Any]) -> models.SnapshotModel:
        snapshot = models.SnapshotModel()
        self._set_attrs_with_js_casing(snapshot, data, "id", "player_id")
        snapshot.created_at = self._dt_from_iso(data["createdAt"])
        snapshot.imported_at = self._dt_from_iso_maybe(data["importedAt"])
        snapshot.data = self.deserialize_snapshot_data(data["data"])
        return snapshot

    def deserialize_snapshot_data(self, data: dict[str, t.Any]) -> models.SnapshotDataModel:
        snapshot_data = models.SnapshotDataModel()

        skills = data["skills"].values()
        snapshot_data.skills = [self.deserialize_skill(s) for s in skills]

        bosses = data["bosses"].values()
        snapshot_data.bosses = [self.deserialize_boss(b) for b in bosses]

        activities = data["activities"].values()
        snapshot_data.activities = [self.deserialize_activity(a) for a in activities]

        computed = data["computed"].values()
        snapshot_data.computed = [self.deserialize_computed_metric(c) for c in computed]

        return snapshot_data

    def deserialize_skill(self, data: dict[str, t.Any]) -> models.SkillModel:
        skill = models.SkillModel()
        skill.metric = enums.Skill.from_str(data["metric"])
        self._set_attrs_with_js_casing(skill, data, "ehp", "rank", "level", "experience")
        return skill

    def deserialize_boss(self, data: dict[str, t.Any]) -> models.BossModel:
        boss = models.BossModel()
        boss.metric = enums.Boss.from_str(data["metric"])
        self._set_attrs_with_js_casing(boss, data, "ehb", "rank", "kills")
        return boss

    def deserialize_activity(self, data: dict[str, t.Any]) -> models.ActivityModel:
        activity = models.ActivityModel()
        activity.metric = enums.Activity.from_str(data["metric"])
        self._set_attrs_with_js_casing(activity, data, "rank", "score")
        return activity

    def deserialize_computed_metric(self, data: dict[str, t.Any]) -> models.ComputedMetricModel:
        computed = models.ComputedMetricModel()
        computed.metric = enums.ComputedMetric.from_str(data["metric"])
        self._set_attrs_with_js_casing(computed, data, "rank", "value")
        return computed

    def deserialize_asserted_player_type(
        self, data: dict[str, t.Any]
    ) -> models.AssertPlayerTypeModel:
        asserted = models.AssertPlayerTypeModel()
        asserted.player = self.deserialize_player(data["player"])
        asserted.changed = data["changed"]
        return asserted
