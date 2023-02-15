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

TransformT = t.Callable[[t.Any], t.Any] | None


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
        self,
        model: t.Any,
        data: dict[str, t.Any],
        *attrs: str,
        transform: TransformT = None,
    ) -> None:
        for attr in attrs:
            if transform:
                setattr(model, attr, transform(data[self._to_js_casing(attr)]))
            else:
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
        player.updated_at = self._dt_from_iso(data["updatedAt"])
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

    def deserialize_minimal_snapshot(self, data: dict[str, t.Any]) -> models.MinimalSnapshotModel:
        snapshot = models.MinimalSnapshotModel()
        self._set_attrs_with_js_casing(snapshot, data, "id", "player_id")
        snapshot.created_at = self._dt_from_iso(data["createdAt"])
        snapshot.imported_at = self._dt_from_iso_maybe(data["importedAt"])
        snapshot.data = self.deserialize_minimal_snapshot_data(data["data"])
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

    def deserialize_minimal_snapshot_data(
        self, data: dict[str, t.Any]
    ) -> models.MinimalSnapshotDataModel:
        snapshot_data = models.MinimalSnapshotDataModel()

        skills = data["skills"].values()
        snapshot_data.skills = [self.deserialize_minimal_skill(s) for s in skills]

        bosses = data["bosses"].values()
        snapshot_data.bosses = [self.deserialize_minimal_boss(b) for b in bosses]

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

    def deserialize_minimal_skill(self, data: dict[str, t.Any]) -> models.MinimalSkillModel:
        skill = models.MinimalSkillModel()
        skill.metric = enums.Skill.from_str(data["metric"])
        self._set_attrs_with_js_casing(skill, data, "rank", "level", "experience")
        return skill

    def deserialize_boss(self, data: dict[str, t.Any]) -> models.BossModel:
        boss = models.BossModel()
        boss.metric = enums.Boss.from_str(data["metric"])
        self._set_attrs_with_js_casing(boss, data, "ehb", "rank", "kills")
        return boss

    def deserialize_minimal_boss(self, data: dict[str, t.Any]) -> models.MinimalBossModel:
        skill = models.MinimalBossModel()
        skill.metric = enums.Boss.from_str(data["metric"])
        self._set_attrs_with_js_casing(skill, data, "rank", "kills")
        return skill

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

    def deserialize_achievement(self, data: dict[str, t.Any]) -> models.AchievementModel:
        achievement = models.AchievementModel()
        achievement.created_at = self._dt_from_iso_maybe(data["createdAt"])
        achievement.metric = enums.Metric.from_str(data["metric"])
        achievement.measure = models.AchievementMeasure.from_str(data["measure"])
        self._set_attrs_with_js_casing(achievement, data, "name", "player_id", "threshold")
        return achievement

    def deserialize_player_achievement_progress(
        self, data: dict[str, t.Any]
    ) -> models.PlayerAchievementProgressModel:
        progress = models.PlayerAchievementProgressModel()
        progress.achievement = self.deserialize_achievement(data)
        self._set_attrs_with_js_casing(
            progress, data, "current_value", "absolute_progress", "relative_progress"
        )

        return progress

    def deserialize_gains(self, data: dict[str, t.Any]) -> models.GainsModel:
        gains = models.GainsModel()
        self._set_attrs_with_js_casing(gains, data, "gained", "start", "end")
        return gains

    def deserialize_skill_gains(self, data: dict[str, t.Any]) -> models.SkillGainsModel:
        gains = models.SkillGainsModel()
        gains.metric = enums.Skill.from_str(data["metric"])
        self._set_attrs_with_js_casing(
            gains, data, "experience", "ehp", "rank", "level", transform=self.deserialize_gains
        )

        return gains

    def deserialize_boss_gains(self, data: dict[str, t.Any]) -> models.BossGainsModel:
        gains = models.BossGainsModel()
        gains.metric = enums.Boss.from_str(data["metric"])
        self._set_attrs_with_js_casing(
            gains, data, "ehb", "rank", "kills", transform=self.deserialize_gains
        )

        return gains

    def deserialize_activity_gains(self, data: dict[str, t.Any]) -> models.ActivityGainsModel:
        gains = models.ActivityGainsModel()
        gains.metric = enums.Activity.from_str(data["metric"])
        self._set_attrs_with_js_casing(
            gains, data, "rank", "score", transform=self.deserialize_gains
        )

        return gains

    def deserialize_computed_gains(self, data: dict[str, t.Any]) -> models.ComputedGainsModel:
        gains = models.ComputedGainsModel()
        gains.metric = enums.ComputedMetric.from_str(data["metric"])
        self._set_attrs_with_js_casing(
            gains, data, "rank", "value", transform=self.deserialize_gains
        )

        return gains

    def deserialize_player_gains_data(self, data: dict[str, t.Any]) -> models.PlayerGainsDataModel:
        gains = models.PlayerGainsDataModel()

        skills = data["skills"].values()
        gains.skills = [self.deserialize_skill_gains(s) for s in skills]

        bosses = data["bosses"].values()
        gains.bosses = [self.deserialize_boss_gains(b) for b in bosses]

        activities = data["activities"].values()
        gains.activities = [self.deserialize_activity_gains(a) for a in activities]

        computed = data["computed"].values()
        gains.computed = [self.deserialize_computed_gains(c) for c in computed]

        return gains

    def deserialize_player_gains(self, data: dict[str, t.Any]) -> models.PlayerGainsModel:
        gains = models.PlayerGainsModel()
        gains.data = self.deserialize_player_gains_data(data["data"])
        self._set_attrs_with_js_casing(
            gains, data, "starts_at", "ends_at", transform=self._dt_from_iso
        )

        return gains

    def deserialize_name_change(self, data: dict[str, t.Any]) -> models.NameChangeModel:
        change = models.NameChangeModel()
        change.status = models.NameChangeStatus.from_str(data["status"])
        change.updated_at = self._dt_from_iso(data["updatedAt"])
        change.created_at = self._dt_from_iso(data["createdAt"])
        change.resolved_at = self._dt_from_iso_maybe(data["createdAt"])
        self._set_attrs_with_js_casing(change, data, "id", "player_id", "old_name", "new_name")
        return change

    def deserialize_name_change_data(self, data: dict[str, t.Any]) -> models.NameChangeDataModel:
        change_data = models.NameChangeDataModel()
        change_data.old_stats = self.deserialize_minimal_snapshot(data["oldStats"])
        change_data.new_stats = self.deserialize_minimal_snapshot(data["newStats"])
        self._set_attrs_with_js_casing(
            change_data,
            data,
            "is_new_on_hiscores",
            "is_old_on_hiscores",
            "has_negative_gains",
            "is_new_tracked",
            "time_diff",
            "hours_diff",
            "ehp_diff",
            "ehb_diff",
        )

        return change_data

    # TODO: Fix deserialization
    #   - Sometimes data["data"] is not present
    #   - When data is present new_stats can be missing an id field
    def deserialize_name_change_detail(
        self, data: dict[str, t.Any]
    ) -> models.NameChangeDetailModel:
        change_detail = models.NameChangeDetailModel()
        change_detail.name_change = self.deserialize_name_change(data["nameChange"])
        change_detail.data = self.deserialize_name_change_data(data["data"])
        return change_detail
