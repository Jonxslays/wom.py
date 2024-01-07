# v1.0.0-rc.1 (Jan 2024)

Stable Release Candidate 1!

## Breaking changes

- Removed internal `wom._cli` module.
- Renamed project info `wompy` cli command to `wom`.

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
