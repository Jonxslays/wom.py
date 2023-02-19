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

T = t.TypeVar("T")
TransformT = t.Callable[[t.Any], t.Any] | None
BaseAchievementT = t.TypeVar("BaseAchievementT", bound=models.BaseAchievementModel)


class Serializer:
    __slots__ = ()

    def _dt_from_iso(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.rstrip("Z"))

    def _dt_from_iso_maybe(self, timestamp: str | None) -> datetime | None:
        return self._dt_from_iso(timestamp) if timestamp else None

    def _to_camel_case(self, attr: str) -> str:
        first, *rest = attr.split("_")
        return "".join((first.lower(), *map(str.title, rest)))

    def _set_attrs(
        self,
        model: t.Any,
        data: dict[str, t.Any],
        *attrs: str,
        transform: TransformT = None,
        camel_case: bool = False,
    ) -> None:
        for attr in attrs:
            cased_attr = self._to_camel_case(attr) if camel_case else attr

            if transform:
                setattr(model, attr, transform(data[cased_attr]))
            else:
                setattr(model, attr, data[cased_attr])

    def _set_attrs_cased(
        self,
        model: t.Any,
        data: dict[str, t.Any],
        *attrs: str,
        transform: TransformT = None,
    ) -> None:
        self._set_attrs(model, data, *attrs, transform=transform, camel_case=True)

    def _deserialize_base_achievement(
        self, model: BaseAchievementT, data: dict[str, t.Any]
    ) -> BaseAchievementT:
        model.metric = enums.Metric.from_str(data["metric"])
        model.measure = models.AchievementMeasure.from_str(data["measure"])
        self._set_attrs_cased(model, data, "name", "player_id", "threshold")
        return model

    def _determine_hiscores_entry_item(
        self, data: dict[str, t.Any]
    ) -> (
        models.GroupHiscoresActivityItemModel
        | models.GroupHiscoresBossItemModel
        | models.GroupHiscoresSkillItemModel
        | models.GroupHiscoresComputedMetricItemModel
    ):
        if "experience" in data:
            return self.deserialize_group_hiscores_skill_item(data)

        if "kills" in data:
            return self.deserialize_group_hiscores_boss_item(data)

        if "score" in data:
            return self.deserialize_group_hiscores_activity_item(data)

        if "value" in data:
            return self.deserialize_group_hiscores_computed_item(data)

        raise ValueError(f"Unknown hiscores entry item: {data}")

    def deserialize_player(self, data: dict[str, t.Any]) -> models.PlayerModel:
        player = models.PlayerModel()
        self._set_attrs_cased(
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
        snapshot.created_at = self._dt_from_iso(data["createdAt"])
        snapshot.imported_at = self._dt_from_iso_maybe(data.get("importedAt"))
        snapshot.data = self.deserialize_snapshot_data(data["data"])
        self._set_attrs_cased(snapshot, data, "id", "player_id")
        return snapshot

    def deserialize_statistics_snapshot(
        self, data: dict[str, t.Any]
    ) -> models.StatisticsSnapshotModel:
        snapshot = models.StatisticsSnapshotModel()
        snapshot.created_at = self._dt_from_iso_maybe(data["createdAt"])
        snapshot.imported_at = self._dt_from_iso_maybe(data.get("importedAt"))
        snapshot.data = self.deserialize_snapshot_data(data["data"])
        self._set_attrs_cased(snapshot, data, "id", "player_id")
        return snapshot

    def gather(
        self, serializer: t.Callable[[dict[str, t.Any]], T], data: list[dict[str, t.Any]]
    ) -> list[T]:
        return [serializer(item) for item in data]

    def deserialize_snapshot_data(self, data: dict[str, t.Any]) -> models.SnapshotDataModel:
        snapshot_data = models.SnapshotDataModel()
        snapshot_data.skills = self.gather(self.deserialize_skill, data["skills"].values())
        snapshot_data.bosses = self.gather(self.deserialize_boss, data["bosses"].values())
        snapshot_data.activities = self.gather(
            self.deserialize_activity, data["activities"].values()
        )

        snapshot_data.computed = self.gather(
            self.deserialize_computed_metric, data["computed"].values()
        )

        return snapshot_data

    def deserialize_skill(self, data: dict[str, t.Any]) -> models.SkillModel:
        skill = models.SkillModel()
        skill.metric = enums.Skill.from_str(data["metric"])
        self._set_attrs(skill, data, "ehp", "rank", "level", "experience")
        return skill

    def deserialize_boss(self, data: dict[str, t.Any]) -> models.BossModel:
        boss = models.BossModel()
        boss.metric = enums.Boss.from_str(data["metric"])
        self._set_attrs(boss, data, "ehb", "rank", "kills")
        return boss

    def deserialize_activity(self, data: dict[str, t.Any]) -> models.ActivityModel:
        activity = models.ActivityModel()
        activity.metric = enums.Activity.from_str(data["metric"])
        self._set_attrs(activity, data, "rank", "score")
        return activity

    def deserialize_computed_metric(self, data: dict[str, t.Any]) -> models.ComputedMetricModel:
        computed = models.ComputedMetricModel()
        computed.metric = enums.ComputedMetric.from_str(data["metric"])
        self._set_attrs(computed, data, "rank", "value")
        return computed

    def deserialize_asserted_player_type(
        self, data: dict[str, t.Any]
    ) -> models.AssertPlayerTypeModel:
        asserted = models.AssertPlayerTypeModel()
        asserted.player = self.deserialize_player(data["player"])
        asserted.changed = data["changed"]
        return asserted

    def deserialize_achievement_progress(
        self, data: dict[str, t.Any]
    ) -> models.AchievementProgressModel:
        achievement = self._deserialize_base_achievement(models.AchievementProgressModel(), data)
        achievement.created_at = self._dt_from_iso_maybe(data["createdAt"])
        return achievement

    def deserialize_achievement(self, data: dict[str, t.Any]) -> models.AchievementModel:
        achievement = self._deserialize_base_achievement(models.AchievementModel(), data)
        achievement.created_at = self._dt_from_iso(data["createdAt"])
        return achievement

    def deserialize_player_achievement_progress(
        self, data: dict[str, t.Any]
    ) -> models.PlayerAchievementProgressModel:
        progress = models.PlayerAchievementProgressModel()
        progress.achievement = self.deserialize_achievement_progress(data)
        self._set_attrs_cased(
            progress, data, "current_value", "absolute_progress", "relative_progress"
        )

        return progress

    def deserialize_gains(self, data: dict[str, t.Any]) -> models.GainsModel:
        gains = models.GainsModel()
        self._set_attrs(gains, data, "gained", "start", "end")
        return gains

    def deserialize_skill_gains(self, data: dict[str, t.Any]) -> models.SkillGainsModel:
        gains = models.SkillGainsModel()
        gains.metric = enums.Skill.from_str(data["metric"])
        self._set_attrs(
            gains, data, "experience", "ehp", "rank", "level", transform=self.deserialize_gains
        )

        return gains

    def deserialize_boss_gains(self, data: dict[str, t.Any]) -> models.BossGainsModel:
        gains = models.BossGainsModel()
        gains.metric = enums.Boss.from_str(data["metric"])
        self._set_attrs(gains, data, "ehb", "rank", "kills", transform=self.deserialize_gains)
        return gains

    def deserialize_activity_gains(self, data: dict[str, t.Any]) -> models.ActivityGainsModel:
        gains = models.ActivityGainsModel()
        gains.metric = enums.Activity.from_str(data["metric"])
        self._set_attrs(gains, data, "rank", "score", transform=self.deserialize_gains)
        return gains

    def deserialize_computed_gains(self, data: dict[str, t.Any]) -> models.ComputedGainsModel:
        gains = models.ComputedGainsModel()
        gains.metric = enums.ComputedMetric.from_str(data["metric"])
        self._set_attrs(gains, data, "rank", "value", transform=self.deserialize_gains)
        return gains

    def deserialize_player_gains_data(self, data: dict[str, t.Any]) -> models.PlayerGainsDataModel:
        gains = models.PlayerGainsDataModel()
        gains.skills = self.gather(self.deserialize_skill_gains, data["skills"].values())
        gains.bosses = self.gather(self.deserialize_boss_gains, data["bosses"].values())
        gains.computed = self.gather(self.deserialize_computed_gains, data["computed"].values())
        gains.activities = self.gather(
            self.deserialize_activity_gains, data["activities"].values()
        )

        return gains

    def deserialize_player_gains(self, data: dict[str, t.Any]) -> models.PlayerGainsModel:
        gains = models.PlayerGainsModel()
        gains.data = self.deserialize_player_gains_data(data["data"])
        self._set_attrs_cased(gains, data, "starts_at", "ends_at", transform=self._dt_from_iso)

        return gains

    def deserialize_name_change(self, data: dict[str, t.Any]) -> models.NameChangeModel:
        change = models.NameChangeModel()
        change.status = models.NameChangeStatus.from_str(data["status"])
        change.updated_at = self._dt_from_iso(data["updatedAt"])
        change.created_at = self._dt_from_iso(data["createdAt"])
        change.resolved_at = self._dt_from_iso_maybe(data["createdAt"])
        self._set_attrs_cased(change, data, "id", "player_id", "old_name", "new_name")
        return change

    def deserialize_name_change_data(self, data: dict[str, t.Any]) -> models.NameChangeDataModel:
        change_data = models.NameChangeDataModel()
        change_data.old_stats = self.deserialize_snapshot(data["oldStats"])
        # NOTE: Hack to handle case where name change details new stats
        # don't have an ID if the new username is not tracked by WOM
        change_data.new_stats = None
        new_stats = data.get("newStats")

        if new_stats:
            if "id" not in new_stats:
                new_stats["id"] = -1

            change_data.new_stats = self.deserialize_snapshot(new_stats)

        self._set_attrs_cased(
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

    def deserialize_name_change_detail(
        self, data: dict[str, t.Any]
    ) -> models.NameChangeDetailModel:
        change_detail = models.NameChangeDetailModel()
        change_detail.name_change = self.deserialize_name_change(data["nameChange"])

        # Data is only present on pending name changes
        change_detail.data = (
            self.deserialize_name_change_data(d) if (d := data.get("data")) else None
        )

        return change_detail

    def deserialize_record(self, data: dict[str, t.Any]) -> models.RecordModel:
        record = models.RecordModel()
        record.period = enums.Period.from_str(data["period"])
        record.metric = enums.Metric.from_str(data["metric"])
        record.updated_at = self._dt_from_iso(data["updatedAt"])
        self._set_attrs_cased(record, data, "id", "player_id", "value")
        return record

    def deserialize_record_leaderboard_entry(
        self, data: dict[str, t.Any]
    ) -> models.RecordLeaderboardEntryModel:
        record = models.RecordLeaderboardEntryModel()
        record.record = self.deserialize_record(data)
        record.player = self.deserialize_player(data["player"])
        return record

    def deserialize_delta_leaderboard_entry(
        self, data: dict[str, t.Any]
    ) -> models.DeltaLeaderboardEntryModel:
        delta = models.DeltaLeaderboardEntryModel()
        delta.gained = data["gained"]
        delta.player_id = data["playerId"]
        delta.end_date = self._dt_from_iso(data["endDate"])
        delta.start_date = self._dt_from_iso(data["startDate"])
        delta.player = self.deserialize_player(data["player"])
        return delta

    def deserialize_group(self, data: dict[str, t.Any]) -> models.GroupModel:
        group = models.GroupModel()
        group.created_at = self._dt_from_iso(data["createdAt"])
        group.updated_at = self._dt_from_iso(data["updatedAt"])
        self._set_attrs_cased(
            group,
            data,
            "id",
            "name",
            "clan_chat",
            "description",
            "homeworld",
            "verified",
            "score",
            "member_count",
        )

        return group

    def deserialize_membership(self, data: dict[str, t.Any]) -> models.MembershipModel:
        membership = models.MembershipModel()
        membership.role = models.GroupRole.from_str_maybe(data["role"])
        membership.created_at = self._dt_from_iso(data["createdAt"])
        membership.updated_at = self._dt_from_iso(data["updatedAt"])
        self._set_attrs_cased(membership, data, "player_id", "group_id")
        return membership

    def deserialize_group_membership(self, data: dict[str, t.Any]) -> models.GroupMembershipModel:
        group = models.GroupMembershipModel()
        group.player = self.deserialize_player(data["player"])
        group.membership = self.deserialize_membership(data)
        return group

    def deserialize_group_details(self, data: dict[str, t.Any]) -> models.GroupDetailModel:
        details = models.GroupDetailModel()
        details.verification_code = None
        details.group = self.deserialize_group(data)
        details.memberships = self.gather(self.deserialize_group_membership, data["memberships"])
        return details

    def deserialize_group_hiscores_activity_item(
        self, data: dict[str, t.Any]
    ) -> models.GroupHiscoresActivityItemModel:
        item = models.GroupHiscoresActivityItemModel()
        self._set_attrs(item, data, "rank", "score")
        return item

    def deserialize_group_hiscores_boss_item(
        self, data: dict[str, t.Any]
    ) -> models.GroupHiscoresBossItemModel:
        item = models.GroupHiscoresBossItemModel()
        self._set_attrs(item, data, "rank", "kills")
        return item

    def deserialize_group_hiscores_skill_item(
        self, data: dict[str, t.Any]
    ) -> models.GroupHiscoresSkillItemModel:
        item = models.GroupHiscoresSkillItemModel()
        self._set_attrs(item, data, "rank", "level", "experience")
        return item

    def deserialize_group_hiscores_computed_item(
        self, data: dict[str, t.Any]
    ) -> models.GroupHiscoresComputedMetricItemModel:
        item = models.GroupHiscoresComputedMetricItemModel()
        self._set_attrs(item, data, "rank", "value")
        return item

    def deserialize_group_hiscores_entry(
        self, data: dict[str, t.Any]
    ) -> models.GroupHiscoresEntryModel:
        hiscores = models.GroupHiscoresEntryModel()
        hiscores.player = self.deserialize_player(data["player"])
        hiscores.data = self._determine_hiscores_entry_item(data["data"])
        return hiscores

    def deserialize_group_statistics(self, data: dict[str, t.Any]) -> models.GroupStatisticsModel:
        statistics = models.GroupStatisticsModel()
        statistics.maxed_200ms_count = data["maxed200msCount"]
        statistics.average_stats = self.deserialize_statistics_snapshot(data["averageStats"])
        self._set_attrs_cased(statistics, data, "maxed_total_count", "maxed_combat_count")
        return statistics

    def deserialize_competition(self, data: dict[str, t.Any]) -> models.CompetitionModel:
        competition = models.CompetitionModel()
        competition.group = self.deserialize_group(data["group"])
        competition.metric = enums.Metric.from_str(data["metric"])
        competition.type = models.CompetitionType.from_str(data["type"])

        self._set_attrs_cased(
            competition,
            data,
            "starts_at",
            "ends_at",
            "created_at",
            "updated_at",
            transform=self._dt_from_iso,
        )

        self._set_attrs_cased(
            competition, data, "id", "title", "group_id", "score", "participant_count"
        )

        return competition
