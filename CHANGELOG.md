# v.2.0.2 (May 2025)
- Add new boss metric `Yama` `(yama)`


# v.2.0.2 (Feb 2025)
- Add new boss metric `Royal Titans` `(the_royal_titans)`

# v2.0 (Jan 2025)

# Breaking

- Drop support for Python 3.8.
- Minimum msgspec version is now `0.19.0`.

## Additions

- Add `CollectionsLogged` metric.
- Add support for Python 3.13.

---

# v1.0.1 (Sep 2024)

## Additions

- Added two new boss metrics `Amoxliatl` and `Hueycoatl`.

---

# v1.0.0 (Sep 2024)

Stable!

## Changes

- `Group.clan_chat` is now optional.

## Bugfixes

- Fix bug where old groups with no clan chat would fail to deserialize.

---

# v1.0.0-rc.2 (Aug 2024)

## Additions

- Added Araxxor to the `Bosses` enum.

---

# v1.0.0-rc.1 (Aug 2024)

Stable Release Candidate 1

10x performance increase when serializing/deserializing models!

## Breaking changes

- Removed internal `wom._cli` module.
- Renamed project info `wompy` cli command to `wom`.
- Models are now `msgspec.Struct` models instead of `attrs` models.
- `PlayerDetail` now inherits from `Player` and so the `player` property was removed.
- `PlayerAchievementProgress` now inherits from `AchievementProgress` and so the
  `achievement` property was removed.
- `PlayerCompetitionStanding` now inherits from `PlayerParticipation` and so the
  `participation` property was removed.
- `GroupMembership` and `PlayerMembership` now inherit from `Membership` and so the
  `membership` property was removed.
- `PlayerArchive` now inherits from `Archive` and so the `archive` property was removed.
- Renamed `RecordService.get_global_record_leaderboards` to `get_global_leaderboards`.
- `RecordLeaderboardEntry` now inherits from `Record` and so the `record` property
  was removed.
- Removed `DeniedNameChangeReviewContext`, and `SkippedNameChangeReviewContext`,
  their properties now live on `NameChangeReviewContext`.
- `CompetitionParticipationDetail` now inherits from `CompetitionParticipation`
  and so the `participation` property was removed.
- `CompetitionDetail` now inherits from `Competition` and so the `competition`
  property was removed.
- `CompetitionService.edit_competition` now returns a `Competition`.
- All methods in the `Serializer` prefixed with `deserialize_` were removed.
- `GroupDetail` now inherits from `Group` and so the `group` property was removed.
- The `verification_code` property on `GroupDetail` was removed.
- Converted the `Skills`, `Activities`, `Bosses`, and `ComputedMetrics` enums
  into `frozenset`s.
- `CompetitionWithParticipations` was renamed to `CreatedCompetitionDetail` because the
  `participations` property was removed and added to `Competition` and the name was no
  longer an accurate representation of the object.
- `EfficiencyService.get_global_leaderboard` was renamed to `get_global_leaderboards`
  to be in line with the other leaderboard method names.
- The `from_str` and `from_str_maybe` methods were removed from the `Metric` enum.

## Additions

- Added `CreatedGroupDetail` model which always has the verification code present.
- Added `previous_role` property to `GroupActivity`.
- Added `CompetitionService.get_details_csv` method.
- Added `MetricLeader` class for the different flavors of leader to derive from.
- Added `CompetitionCSVTableType` enum for the competition details csv endpoint.
- Added pagination to `PlayerService.get_snapshots`.

## Changes

- `Record.value` is now a `float` instead of an `int`.
- `ComputedMetricLeader.value` is now a `float` instead of an `int`.
- The `Metric` enum now includes all variants of the old `Skills`, `Activities`,
  `Bosses`, and `ComputedMetrics` enums.
- `GroupService.create_group` now returns a `CreatedGroupDetail` model.
- Updated docstrings for group classes.
- Fixed broken poetry install link in contributing guide.

---

# v0.9.5 (Mar 2024)

## Additions

- Add varlamore metrics (ColosseumGlory, LunarChests, SolHeredit).

---

# v0.9.4 (Mar 2024)

## Bugfixes

- Fix bug where `PlayerDetail` with no latest snapshot would fail to deserialize.

---

# v0.9.3 (Jan 2024)

## Additions

- Add `Scurrius` to `Bosses`.

---

# v0.9.2 (Jan 2024)

## Additions

- Add `archive` property to `PlayerDetail`.
- Add `Archive` and `PlayerArchive` models/serialization methods.
- Add `get_archives` method to `PlayerService`.
- Add `to_dict` method to `Result`.

## Fixes

- Fix some Python 3.8 incompatible type hints.

---

# v0.9.1 (Nov 2023)

## Bugfixes

- Fix invalid key regression for social links.

---

# v0.9.0 (Nov 2023)

## Additions

- Add `at_random` method to `BaseEnum` for generating an enum variant at random.
- Add `levels` property to `CompetitionParticipationDetail`.
- Add `patron`, `banner_image`, and `profile_image` properties to `Group`.
- Add `SocialLinks` model and `social_links` property to `GroupDetail`.
- Add getting started guide to the documentation.

## Changes

- Methods that previously accepted only `GroupMemberFragment` now accept strings as well.
- Update examples in `GroupService` that work with `GroupMemberFragment`.
- Remove usage of weakref slots throughout the project, improving memory footprint.

---

# v0.8.1 (Nov 2023)

## Additions

- Add `rank` property to `SnapshotTimelineEntry`.

---

# v0.8.0 (Oct 2023)

## Additions

- Add `GroupActivity` and `GroupActivityType` models.
- Add `deserialize_group_activity` serializer method.
- Add `get_activity` group service method.
- Add `GROUP_ACTIVITY` Route.

---

# v0.7.0 (Oct 2023)

## Changes

- `Player.updated_at` is now optional.

## Additions

- Add `FailedToDeserialize` error.

## Fixes

- Fix typo in docstring for `PlayerService.get_records`.

---

# v0.6.1 (Sep 2023)

## Additions

- Add `F2P Lvl 3` player build.

---

# v0.6.0 (Jul 2023)

## Additions

- Add support for Desert Treasure 2 bosses.

---

# v0.5.0 (Jul 2023)

## Additions

- Add `PlayerService.get_snapshots_timeline` method.
- Add `SnapshotTimelineEntry` model and corresponding serializer method.
- Add `GroupMemberGains` model and corresponding serializer method.

## Changes

- `GroupService.get_gains` method now returns a `GroupMemberGains` model.

---

# v0.4.2 (Jun 2023)

## Additions

- Add `Banned` player status.
- Add helpful error message if new enum variants are not yet added to the lib.

---

# v0.4.1 (May 2023)

## Breaking Changes

- Make `MetricLeaders.player` optional, indicating no player leads in the metric.
- Fix typos in the `Bosses` enum.

---

# v0.4.0 (May 2023)

## Breaking Changes

- Remove `NameChangeService.get_name_change_details` as it is no longer supported by WOM.
- Remove models and serialization methods associated with the above method.

## Additions

- Add new `review_context` field to `NameChange`.
- Add `NameChangeReviewContext`, `SkippedNameChangeReviewContext`, and
  `DeniedNameChangeReviewContext` models.
- Add `NameChangeReviewReason` enum.
- Add serialization method for the above models.

## Bugfixes

- Fix support for Python 3.8 and 3.9 by using older style type hints.

---

# v0.3.3 (Apr 2023)

## Bugfixes

- Fix bug in `Route` that caused requests to be made to incorrect URI's.

---

# v0.3.2 (Apr 2023)

## Breaking Changes

- Add a new _required_ async `Client.start` method to fix deprecation warning emitted
  by creating a `ClientSession` in a non-async function.

---

# v0.3.1 (Apr 2023)

## Additions

- Add new wildy bosses Artio, Calvarion, and Spindel to the `Bosses` enum.

---

# v0.3.0 (Apr 2023)

## Breaking Changes

- `MetricLeaders`, `PlayerGainsData`, and `SnapshotData` now contain mappings of their
  `enums.Skills` key to values of the associated type that was previously contained in the list.
- The deserialization methods associated with the above types were also updated to accommodate
  this.
- the `Player.flagged` field was removed in favor of the `Player.status` field.

## Changes

- Only include the type of the value, not the value itself, in the error message raised when
  calling `unwrap_err` on an `Ok` variant.
- `Skill.ehp`, `Boss.ehb`, and `ComputedMetric.value` are now `float` type.

## Additions

- Tests! :eyes:
- A `PlayerStatus` enum representing the statuses a player can be in (flagged, active, etc)

---

# v0.2.0 (Feb 2023)

## Breaking Changes

- `GroupStatistics.average_stats` is now a `Snapshot` rather than a `GroupSnapshot`.
- Remove `GroupSnapshot` model since `created_at` on `Snapshot` is now guaranteed to be present.

## Bugfixes

- Add some missing models to `__all__`.

## Additions

- Add leaders models: `SkillLeader`, `BossLeader`, `ActivityLeader`, `ComputedMetricLeader`,
  and `MetricLeaders`.
- Add `metric_leaders` property to `GroupStatistics`.
- Add deserialization methods for the new leader models.

---

# v0.1.1 (Feb 2023)

## Bugfixes

- `EfficiencyService.get_global_leaderboard` now accepts a `both` kwarg, and will no longer
  erroneously allow you to pass many computed metrics as `*args`.

## Changes

- Relaxed the pinned dependencies for better compatibility.
- The `metric` parameter to `EfficiencyService.get_global_leaderboard` is now defaulted to EHP.

---

# v0.1.0 (Feb 2023)

- Initial release!
