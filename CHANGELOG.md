# v0.2.0 (Feb 2023)

## Bugfixes

- Add some missing models to `__all__`.

## Additions

- Add leaders models: `SkillLeader`, `BossLeader`, `ActivityLeader`, `ComputedMetricLeader`, and
  `MetricLeaders`.
- Add `metric_leaders` property to `GroupStatistics`.
- Add deserialization methods for the new leader models.

## Changes

- `GroupStatistics.average_stats` is now a `Snapshot` rather than a `GroupSnapshot`.

## Removals

- Remove `GroupSnapshot` model since `created_at` on `Snapshot` is now guaranteed to be present.

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
