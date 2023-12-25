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

"""This module contains the [`Serializer`][wom.serializer.Serializer]
that is used to parse incoming network data into Python classes.
"""

from __future__ import annotations

import functools
import typing as t
from datetime import datetime

from wom import enums
from wom import errors
from wom import models

__all__ = ("Serializer",)

T = t.TypeVar("T")
DictT = t.Dict[str, t.Any]
TransformT = t.Optional[t.Callable[[t.Any], t.Any]]
SerializerT = t.Callable[["Serializer", DictT], T]
AchievementT = t.TypeVar("AchievementT", models.Achievement, models.AchievementProgress)
HasMetricsT = t.TypeVar(
    "HasMetricsT",
    models.Skill,
    models.Boss,
    models.Activity,
    models.ComputedMetric,
    models.SkillLeader,
    models.BossLeader,
    models.ActivityLeader,
    models.ComputedMetricLeader,
    models.SkillGains,
    models.BossGains,
    models.ActivityGains,
    models.ComputedGains,
)


def serializer_guard(deserialize: SerializerT[T]) -> SerializerT[T]:
    @functools.wraps(deserialize)
    def wrapper(serializer: Serializer, data: DictT) -> T:
        try:
            return deserialize(serializer, data)
        except Exception as e:
            raise errors.FailedToDeserialize(deserialize, e) from None

    return wrapper


class Serializer:
    """Deserializes JSON data into wom.py model classes."""

    __slots__ = ()

    def _dt_from_iso(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp.rstrip("Z"))

    def _dt_from_iso_maybe(self, timestamp: t.Optional[str]) -> t.Optional[datetime]:
        return self._dt_from_iso(timestamp) if timestamp else None

    def _to_camel_case(self, attr: str) -> str:
        first, *rest = attr.split("_")
        return "".join((first.lower(), *map(str.title, rest)))

    def __map(
        self, serializer: t.Callable[[DictT], HasMetricsT], data: t.List[DictT]
    ) -> t.Dict[t.Any, HasMetricsT]:
        return {x.metric: x for x in (serializer(y) for y in data)}

    def _set_attrs(
        self,
        model: t.Any,
        data: DictT,
        *attrs: str,
        transform: TransformT = None,
        camel_case: bool = False,
        maybe: bool = False,
    ) -> None:
        if transform and maybe:
            raise RuntimeError("Only one of 'maybe' and 'transform' may be used.")

        for attr in attrs:
            cased_attr = self._to_camel_case(attr) if camel_case else attr

            if transform:
                setattr(
                    model,
                    attr,
                    transform(data.get(cased_attr, None) if maybe else data[cased_attr]),
                )
            else:
                setattr(model, attr, data.get(cased_attr, None) if maybe else data[cased_attr])

    def _set_attrs_cased(
        self,
        model: t.Any,
        data: DictT,
        *attrs: str,
        transform: TransformT = None,
        maybe: bool = False,
    ) -> None:
        self._set_attrs(model, data, *attrs, transform=transform, camel_case=True, maybe=maybe)

    def _deserialize_base_achievement(self, model: AchievementT, data: DictT) -> AchievementT:
        model.metric = enums.Metric.from_str(data["metric"])
        model.measure = models.AchievementMeasure.from_str(data["measure"])
        self._set_attrs_cased(model, data, "name", "player_id", "threshold", "accuracy")
        return model

    def _determine_hiscores_entry_item(
        self, data: DictT
    ) -> t.Union[
        models.GroupHiscoresActivityItem,
        models.GroupHiscoresBossItem,
        models.GroupHiscoresSkillItem,
        models.GroupHiscoresComputedMetricItem,
    ]:
        if "experience" in data:
            return self.deserialize_group_hiscores_skill_item(data)

        if "kills" in data:
            return self.deserialize_group_hiscores_boss_item(data)

        if "score" in data:
            return self.deserialize_group_hiscores_activity_item(data)

        if "value" in data:
            return self.deserialize_group_hiscores_computed_item(data)

        raise ValueError(f"Unknown hiscores entry item: {data}")

    @serializer_guard
    def deserialize_player(self, data: DictT) -> models.Player:
        """Deserializes the data into a player model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        player = models.Player()
        self._set_attrs_cased(
            player,
            data,
            "id",
            "username",
            "display_name",
            "exp",
            "ehp",
            "ehb",
            "ttm",
            "tt200m",
        )

        player.type = models.PlayerType.from_str(data["type"])
        player.build = models.PlayerBuild.from_str(data["build"])
        player.status = models.PlayerStatus.from_str(data["status"])
        player.country = models.Country.from_str_maybe(data["country"])
        player.registered_at = self._dt_from_iso(data["registeredAt"])
        player.updated_at = self._dt_from_iso_maybe(data["updatedAt"])
        player.last_changed_at = self._dt_from_iso_maybe(data["lastChangedAt"])
        player.last_imported_at = self._dt_from_iso_maybe(data["lastImportedAt"])
        return player

    @serializer_guard
    def deserialize_player_details(self, data: DictT) -> models.PlayerDetail:
        """Deserializes the data into a player detail model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        details = models.PlayerDetail()
        details.combat_level = data["combatLevel"]
        details.player = self.deserialize_player(data)
        details.latest_snapshot = self.deserialize_snapshot(data["latestSnapshot"])

        if archive := data.get("archive"):
            details.archive = self.deserialize_archive(archive)
        else:
            details.archive = None

        return details

    @serializer_guard
    def deserialize_snapshot(self, data: DictT) -> models.Snapshot:
        """Deserializes the data into a snapshot model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        snapshot = models.Snapshot()
        snapshot.created_at = self._dt_from_iso(data["createdAt"])
        snapshot.imported_at = self._dt_from_iso_maybe(data.get("importedAt"))
        snapshot.data = self.deserialize_snapshot_data(data["data"])
        self._set_attrs_cased(snapshot, data, "id", "player_id")
        return snapshot

    @serializer_guard
    def deserialize_snapshot_data(self, data: DictT) -> models.SnapshotData:
        """Deserializes the data into a snapshot data model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        model = models.SnapshotData()
        model.skills = self.__map(self.deserialize_skill, data["skills"].values())
        model.bosses = self.__map(self.deserialize_boss, data["bosses"].values())
        model.activities = self.__map(self.deserialize_activity, data["activities"].values())
        model.computed = self.__map(self.deserialize_computed_metric, data["computed"].values())
        return model

    @serializer_guard
    def deserialize_skill(self, data: DictT) -> models.Skill:
        """Deserializes the data into a skill model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        skill = models.Skill()
        skill.metric = enums.Skills.from_str(data["metric"])
        self._set_attrs(skill, data, "ehp", "rank", "level", "experience")
        return skill

    @serializer_guard
    def deserialize_boss(self, data: DictT) -> models.Boss:
        """Deserializes the data into a boss model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        boss = models.Boss()
        boss.metric = enums.Bosses.from_str(data["metric"])
        self._set_attrs(boss, data, "ehb", "rank", "kills")
        return boss

    @serializer_guard
    def deserialize_activity(self, data: DictT) -> models.Activity:
        """Deserializes the data into an activity model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        activity = models.Activity()
        activity.metric = enums.Activities.from_str(data["metric"])
        self._set_attrs(activity, data, "rank", "score")
        return activity

    @serializer_guard
    def deserialize_computed_metric(self, data: DictT) -> models.ComputedMetric:
        """Deserializes the data into a computed metric model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        computed = models.ComputedMetric()
        computed.metric = enums.ComputedMetrics.from_str(data["metric"])
        self._set_attrs(computed, data, "rank", "value")
        return computed

    @serializer_guard
    def deserialize_asserted_player_type(self, data: DictT) -> models.AssertPlayerType:
        """Deserializes the data into an assert player type model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        asserted = models.AssertPlayerType()
        asserted.player = self.deserialize_player(data["player"])
        asserted.changed = data["changed"]
        return asserted

    @serializer_guard
    def deserialize_achievement_progress(self, data: DictT) -> models.AchievementProgress:
        """Deserializes the data into an achievement progress model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        achievement = self._deserialize_base_achievement(models.AchievementProgress(), data)
        achievement.created_at = self._dt_from_iso_maybe(data["createdAt"])
        return achievement

    @serializer_guard
    def deserialize_achievement(self, data: DictT) -> models.Achievement:
        """Deserializes the data into an achievement model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        achievement = self._deserialize_base_achievement(models.Achievement(), data)
        achievement.created_at = self._dt_from_iso(data["createdAt"])
        return achievement

    @serializer_guard
    def deserialize_player_achievement_progress(
        self, data: DictT
    ) -> models.PlayerAchievementProgress:
        """Deserializes the data into a player achievement progress
        model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        progress = models.PlayerAchievementProgress()
        progress.achievement = self.deserialize_achievement_progress(data)
        self._set_attrs_cased(
            progress, data, "current_value", "absolute_progress", "relative_progress"
        )

        return progress

    @serializer_guard
    def deserialize_gains(self, data: DictT) -> models.Gains:
        """Deserializes the data into a gains model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.Gains()
        self._set_attrs(gains, data, "gained", "start", "end")
        return gains

    @serializer_guard
    def deserialize_skill_gains(self, data: DictT) -> models.SkillGains:
        """Deserializes the data into a skill gains model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.SkillGains()
        gains.metric = enums.Skills.from_str(data["metric"])
        self._set_attrs(
            gains, data, "experience", "ehp", "rank", "level", transform=self.deserialize_gains
        )

        return gains

    @serializer_guard
    def deserialize_boss_gains(self, data: DictT) -> models.BossGains:
        """Deserializes the data into a boss gains model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.BossGains()
        gains.metric = enums.Bosses.from_str(data["metric"])
        self._set_attrs(gains, data, "ehb", "rank", "kills", transform=self.deserialize_gains)
        return gains

    @serializer_guard
    def deserialize_activity_gains(self, data: DictT) -> models.ActivityGains:
        """Deserializes the data into an activity gains model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.ActivityGains()
        gains.metric = enums.Activities.from_str(data["metric"])
        self._set_attrs(gains, data, "rank", "score", transform=self.deserialize_gains)
        return gains

    @serializer_guard
    def deserialize_computed_gains(self, data: DictT) -> models.ComputedGains:
        """Deserializes the data into a computed gains model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.ComputedGains()
        gains.metric = enums.ComputedMetrics.from_str(data["metric"])
        self._set_attrs(gains, data, "rank", "value", transform=self.deserialize_gains)
        return gains

    @serializer_guard
    def deserialize_player_gains_data(self, data: DictT) -> models.PlayerGainsData:
        """Deserializes the data into a player gains data model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.PlayerGainsData()
        gains.skills = self.__map(self.deserialize_skill_gains, data["skills"].values())
        gains.bosses = self.__map(self.deserialize_boss_gains, data["bosses"].values())
        gains.computed = self.__map(self.deserialize_computed_gains, data["computed"].values())
        gains.activities = self.__map(self.deserialize_activity_gains, data["activities"].values())
        return gains

    @serializer_guard
    def deserialize_player_gains(self, data: DictT) -> models.PlayerGains:
        """Deserializes the data into a player gains model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.PlayerGains()
        gains.data = self.deserialize_player_gains_data(data["data"])
        self._set_attrs_cased(gains, data, "starts_at", "ends_at", transform=self._dt_from_iso)

        return gains

    @serializer_guard
    def deserialize_name_change_review_context(
        self, data: DictT
    ) -> models.NameChangeReviewContext:
        """Deserializes the data into a name change review context.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        ctx: models.NameChangeReviewContext
        reason = models.NameChangeReviewReason.from_str(data["reason"])

        skipped_reasons = (
            models.NameChangeReviewReason.TransitionTooLong,
            models.NameChangeReviewReason.ExcessiveGains,
            models.NameChangeReviewReason.TotalLevelTooLow,
        )

        denied_reasons = (
            models.NameChangeReviewReason.ManualReview,
            models.NameChangeReviewReason.OldStatsNotFound,
            models.NameChangeReviewReason.NewNameNotFound,
            models.NameChangeReviewReason.NegativeGains,
        )

        if reason in skipped_reasons:
            ctx = models.SkippedNameChangeReviewContext()
            ctx.reason = reason  # type: ignore[assignment]
            self._set_attrs_cased(
                ctx,
                data,
                "max_hours_diff",
                "hours_diff",
                "ehp_diff",
                "ehb_diff",
                "min_total_level",
                "total_level",
                maybe=True,
            )
        elif reason in denied_reasons:
            ctx = models.DeniedNameChangeReviewContext()
            ctx.reason = reason  # type: ignore[assignment]
            ctx.negative_gains = None

            if reason is models.NameChangeReviewReason.NegativeGains:
                negative_gains: t.Dict[enums.Metric, int] = {}

                for metric, value in data["negativeGains"].items():
                    negative_gains[enums.Metric.from_str(metric)] = value

                ctx.negative_gains = negative_gains
        else:
            raise RuntimeError("Unreachable code reached! Serializer::name_change_review_context")

        return ctx

    @serializer_guard
    def deserialize_name_change(self, data: DictT) -> models.NameChange:
        """Deserializes the data into a name change model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        change = models.NameChange()
        change.status = models.NameChangeStatus.from_str(data["status"])
        change.updated_at = self._dt_from_iso(data["updatedAt"])
        change.created_at = self._dt_from_iso(data["createdAt"])
        change.resolved_at = self._dt_from_iso_maybe(data["createdAt"])
        self._set_attrs_cased(change, data, "id", "player_id", "old_name", "new_name")

        if review_context := data.get("reviewContext", None):
            change.review_context = self.deserialize_name_change_review_context(review_context)
        else:
            change.review_context = review_context

        return change

    @serializer_guard
    def deserialize_record(self, data: DictT) -> models.Record:
        """Deserializes the data into a record model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        record = models.Record()
        record.period = enums.Period.from_str(data["period"])
        record.metric = enums.Metric.from_str(data["metric"])
        record.updated_at = self._dt_from_iso(data["updatedAt"])
        self._set_attrs_cased(record, data, "id", "player_id", "value")
        return record

    @serializer_guard
    def deserialize_record_leaderboard_entry(self, data: DictT) -> models.RecordLeaderboardEntry:
        """Deserializes the data into a record leaderboard entry model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        record = models.RecordLeaderboardEntry()
        record.record = self.deserialize_record(data)
        record.player = self.deserialize_player(data["player"])
        return record

    @serializer_guard
    def deserialize_delta_leaderboard_entry(self, data: DictT) -> models.DeltaLeaderboardEntry:
        """Deserializes the data into a delta leaderboard entry  model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        delta = models.DeltaLeaderboardEntry()
        delta.gained = data["gained"]
        delta.player_id = data["playerId"]
        delta.end_date = self._dt_from_iso(data["endDate"])
        delta.start_date = self._dt_from_iso(data["startDate"])
        delta.player = self.deserialize_player(data["player"])
        return delta

    @serializer_guard
    def deserialize_group_member_gains(self, data: DictT) -> models.GroupMemberGains:
        """Deserializes the data into a group member gains model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        gains = models.GroupMemberGains()
        gains.end_date = self._dt_from_iso(data["endDate"])
        gains.start_date = self._dt_from_iso(data["startDate"])
        gains.player = self.deserialize_player(data["player"])
        gains.data = self.deserialize_gains(data["data"])
        return gains

    @serializer_guard
    def deserialize_group(self, data: DictT) -> models.Group:
        """Deserializes the data into a group model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        group = models.Group()
        group.created_at = self._dt_from_iso(data["createdAt"])
        group.updated_at = self._dt_from_iso(data["updatedAt"])
        self._set_attrs_cased(group, data, "profile_image", "banner_image", maybe=True)
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
            "patron",
        )

        return group

    @serializer_guard
    def deserialize_membership(self, data: DictT) -> models.Membership:
        """Deserializes the data into a membership model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        membership = models.Membership()
        membership.role = models.GroupRole.from_str_maybe(data["role"])
        membership.created_at = self._dt_from_iso(data["createdAt"])
        membership.updated_at = self._dt_from_iso(data["updatedAt"])
        self._set_attrs_cased(membership, data, "player_id", "group_id")
        return membership

    @serializer_guard
    def deserialize_group_membership(self, data: DictT) -> models.GroupMembership:
        """Deserializes the data into a group membership model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        group = models.GroupMembership()
        group.player = self.deserialize_player(data["player"])
        group.membership = self.deserialize_membership(data)
        return group

    @serializer_guard
    def deserialize_group_details(self, data: DictT) -> models.GroupDetail:
        """Deserializes the data into a group detail model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        details = models.GroupDetail()
        details.verification_code = None
        details.group = self.deserialize_group(data)
        details.memberships = [self.deserialize_group_membership(m) for m in data["memberships"]]
        details.social_links = self.deserialize_social_links(data["socialLinks"])
        return details

    @serializer_guard
    def deserialize_group_hiscores_activity_item(
        self, data: DictT
    ) -> models.GroupHiscoresActivityItem:
        """Deserializes the data into a group hiscores activity item
        model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        item = models.GroupHiscoresActivityItem()
        self._set_attrs(item, data, "rank", "score")
        return item

    @serializer_guard
    def deserialize_group_hiscores_boss_item(self, data: DictT) -> models.GroupHiscoresBossItem:
        """Deserializes the data into a group hiscores boss item model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        item = models.GroupHiscoresBossItem()
        self._set_attrs(item, data, "rank", "kills")
        return item

    @serializer_guard
    def deserialize_group_hiscores_skill_item(self, data: DictT) -> models.GroupHiscoresSkillItem:
        """Deserializes the data into a group hiscores skill item model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        item = models.GroupHiscoresSkillItem()
        self._set_attrs(item, data, "rank", "level", "experience")
        return item

    @serializer_guard
    def deserialize_group_hiscores_computed_item(
        self, data: DictT
    ) -> models.GroupHiscoresComputedMetricItem:
        """Deserializes the data into a group hiscores computed metric
        item model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        item = models.GroupHiscoresComputedMetricItem()
        self._set_attrs(item, data, "rank", "value")
        return item

    @serializer_guard
    def deserialize_group_hiscores_entry(self, data: DictT) -> models.GroupHiscoresEntry:
        """Deserializes the data into a group hiscores entry model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        hiscores = models.GroupHiscoresEntry()
        hiscores.player = self.deserialize_player(data["player"])
        hiscores.data = self._determine_hiscores_entry_item(data["data"])
        return hiscores

    @serializer_guard
    def deserialize_group_statistics(self, data: DictT) -> models.GroupStatistics:
        """Deserializes the data into a group statistics model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        statistics = models.GroupStatistics()
        statistics.maxed_200ms_count = data["maxed200msCount"]
        statistics.average_stats = self.deserialize_snapshot(data["averageStats"])
        statistics.metric_leaders = self.deserialize_metric_leaders(data["metricLeaders"])
        self._set_attrs_cased(statistics, data, "maxed_total_count", "maxed_combat_count")
        return statistics

    @serializer_guard
    def deserialize_competition(self, data: DictT) -> models.Competition:
        """Deserializes the data into a competition model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        competition = models.Competition()
        competition.metric = enums.Metric.from_str(data["metric"])
        competition.type = models.CompetitionType.from_str(data["type"])
        competition.group = self.deserialize_group(g) if (g := data.get("group")) else None

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

    @serializer_guard
    def deserialize_participation(self, data: DictT) -> models.Participation:
        """Deserializes the data into a participation model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        participation = models.Participation()
        participation.created_at = self._dt_from_iso(data["createdAt"])
        participation.updated_at = self._dt_from_iso(data["updatedAt"])
        self._set_attrs_cased(participation, data, "player_id", "competition_id", "team_name")
        return participation

    @serializer_guard
    def deserialize_player_participation(self, data: DictT) -> models.PlayerParticipation:
        """Deserializes the data into a player participation model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        player_participation = models.PlayerParticipation()
        player_participation.competition = self.deserialize_competition(data["competition"])
        player_participation.data = self.deserialize_participation(data)
        return player_participation

    @serializer_guard
    def deserialize_competition_participation(
        self, data: DictT
    ) -> models.CompetitionParticipation:
        """Deserializes the data into a competition participation model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        competition_participation = models.CompetitionParticipation()
        competition_participation.player = self.deserialize_player(data["player"])
        competition_participation.data = self.deserialize_participation(data)
        return competition_participation

    @serializer_guard
    def deserialize_competition_progress(self, data: DictT) -> models.CompetitionProgress:
        """Deserializes the data into a competition progress model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        progress = models.CompetitionProgress()
        self._set_attrs(progress, data, "start", "end", "gained")
        return progress

    @serializer_guard
    def deserialize_player_competition_standing(
        self, data: DictT
    ) -> models.PlayerCompetitionStanding:
        """Deserializes the data into a player competition standing
        model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        standing = models.PlayerCompetitionStanding()
        standing.rank = data["rank"]
        standing.participation = self.deserialize_player_participation(data)
        standing.progress = self.deserialize_competition_progress(data["progress"])
        return standing

    @serializer_guard
    def deserialize_player_membership(self, data: DictT) -> models.PlayerMembership:
        """Deserializes the data into a player membership model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        player_membership = models.PlayerMembership()
        player_membership.group = self.deserialize_group(data["group"])
        player_membership.membership = self.deserialize_membership(data)
        return player_membership

    @serializer_guard
    def deserialize_competition_details(self, data: DictT) -> models.CompetitionDetail:
        """Deserializes the data into a competition detail model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        details = models.CompetitionDetail()
        details.competition = self.deserialize_competition(data)
        details.participations = [
            self.deserialize_competition_participation_detail(d) for d in data["participations"]
        ]

        return details

    @serializer_guard
    def deserialize_competition_participation_detail(
        self, data: DictT
    ) -> models.CompetitionParticipationDetail:
        """Deserializes the data into a competition participation
        detail model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        details = models.CompetitionParticipationDetail()
        details.participation = self.deserialize_competition_participation(data)
        details.progress = self.deserialize_competition_progress(data["progress"])
        details.levels = self.deserialize_competition_progress(data["levels"])
        return details

    @serializer_guard
    def deserialize_competition_history_data_point(
        self, data: DictT
    ) -> models.CompetitionHistoryDataPoint:
        """Deserializes the data into a competition history data point
        model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        datapoint = models.CompetitionHistoryDataPoint()
        datapoint.date = self._dt_from_iso(data["date"])
        datapoint.value = data["value"]
        return datapoint

    @serializer_guard
    def deserialize_top5_progress_result(self, data: DictT) -> models.Top5ProgressResult:
        """Deserializes the data into a top 5 progress result model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        progress = models.Top5ProgressResult()
        progress.player = self.deserialize_player(data["player"])
        progress.history = [
            self.deserialize_competition_history_data_point(h) for h in data["history"]
        ]

        return progress

    @serializer_guard
    def deserialize_competition_with_participation(
        self, data: DictT
    ) -> models.CompetitionWithParticipations:
        """Deserializes the data into a competition with participations
        model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        model = models.CompetitionWithParticipations()
        model.verification_code = data.get("verificationCode")
        model.competition = self.deserialize_competition(data)
        model.participations = [
            self.deserialize_competition_participation(p) for p in data["participations"]
        ]

        return model

    @serializer_guard
    def deserialize_skill_leader(self, data: DictT) -> models.SkillLeader:
        """Deserializes the data into a skill leader model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        leader = models.SkillLeader()
        leader.metric = enums.Skills.from_str(data["metric"])
        self._set_attrs(leader, data, "experience", "rank", "level")

        if player := data.get("player", None):
            leader.player = self.deserialize_player(player)
        else:
            leader.player = player

        return leader

    @serializer_guard
    def deserialize_boss_leader(self, data: DictT) -> models.BossLeader:
        """Deserializes the data into a boss leader model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        leader = models.BossLeader()
        leader.metric = enums.Bosses.from_str(data["metric"])
        self._set_attrs(leader, data, "kills", "rank")

        if player := data.get("player", None):
            leader.player = self.deserialize_player(player)
        else:
            leader.player = player

        return leader

    @serializer_guard
    def deserialize_activity_leader(self, data: DictT) -> models.ActivityLeader:
        """Deserializes the data into an activity leader model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        leader = models.ActivityLeader()
        leader.metric = enums.Activities.from_str(data["metric"])
        self._set_attrs(leader, data, "score", "rank")

        if player := data.get("player", None):
            leader.player = self.deserialize_player(player)
        else:
            leader.player = player

        return leader

    @serializer_guard
    def deserialize_computed_leader(self, data: DictT) -> models.ComputedMetricLeader:
        """Deserializes the data into a computed metric leader model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        leader = models.ComputedMetricLeader()
        leader.metric = enums.ComputedMetrics.from_str(data["metric"])
        self._set_attrs(leader, data, "value", "rank")

        if player := data.get("player", None):
            leader.player = self.deserialize_player(player)
        else:
            leader.player = player

        return leader

    @serializer_guard
    def deserialize_metric_leaders(self, data: DictT) -> models.MetricLeaders:
        """Deserializes the data into a metric leaders model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        leaders = models.MetricLeaders()
        leaders.skills = self.__map(self.deserialize_skill_leader, data["skills"].values())
        leaders.bosses = self.__map(self.deserialize_boss_leader, data["bosses"].values())
        leaders.computed = self.__map(self.deserialize_computed_leader, data["computed"].values())
        leaders.activities = self.__map(
            self.deserialize_activity_leader, data["activities"].values()
        )

        return leaders

    @serializer_guard
    def deserialize_snapshot_timeline_entry(self, data: DictT) -> models.SnapshotTimelineEntry:
        """Deserializes the data into a snapshot timeline entry model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        entry = models.SnapshotTimelineEntry()
        entry.date = self._dt_from_iso(data["date"])
        self._set_attrs(entry, data, "value", "rank")
        return entry

    @serializer_guard
    def deserialize_group_activity(self, data: DictT) -> models.GroupActivity:
        """Deserializes the data into a group activity model.

        Args:
            data: The JSON payload.

        Returns:
            The requested model.
        """
        activity = models.GroupActivity()
        activity.role = models.GroupRole.from_str_maybe(data["role"])
        activity.player = self.deserialize_player(data["player"])
        activity.created_at = self._dt_from_iso(data["createdAt"])
        activity.type = models.GroupActivityType.from_str(data["type"])
        self._set_attrs_cased(activity, data, "group_id", "player_id")
        return activity

    @serializer_guard
    def deserialize_social_links(self, data: DictT) -> models.SocialLinks:
        return models.SocialLinks(
            website=data.get("website"),
            discord=data.get("discord"),
            youtube=data.get("youtube"),
            twitter=data.get("twitter"),
            twitch=data.get("twitch"),
        )

    @serializer_guard
    def deserialize_archive(self, data: DictT) -> models.Archive:
        archive = models.Archive()
        archive.restored_at = self._dt_from_iso_maybe(data.get("restoredAt"))
        archive.created_at = self._dt_from_iso(data["createdAt"])
        archive.restored_username = data.get("restoredUsername")
        self._set_attrs_cased(archive, data, "archive_username", "player_id", "previous_username")
        return archive

    @serializer_guard
    def deserialize_player_archive(self, data: DictT) -> models.PlayerArchive:
        archive = models.PlayerArchive()
        archive.archive = self.deserialize_archive(data)
        archive.player = self.deserialize_player(data["player"])
        return archive
