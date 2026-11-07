---
name: sync-enums
description: Add a new metric (boss, skill, activity, computed metric) or other enum value to wom.py, or sync every enum against the upstream Wise Old Man source. Use when the user says "add <boss> metric", "add support for <boss>", "add the <country> country", "a new boss released", or "sync enums with upstream".
---

# Sync enums with upstream

Adding a metric is the most common change in this repo (Fractured Archive,
Maggot King, Mad Angel, Brutus, Sailing, ...). Missing `Country` values have
also had to be filled in more than once. Always take enum values from the
upstream source, never guess them.

## Upstream source of truth

Repo `wise-old-man/wise-old-man`, branch `master`, files under
`server/src/types/`. Read them with `gh api`:

```bash
gh api repos/wise-old-man/wise-old-man/contents/server/src/types/metric.enum.ts --jq .content | base64 -d
```

| Upstream file                          | wom.py enum                                  |
| -------------------------------------- | -------------------------------------------- |
| `metric.enum.ts`                       | `Metric` + the frozensets in `wom/enums.py`  |
| `period.enum.ts`                       | `Period` (`wom/enums.py`)                    |
| `country.enum.ts`                      | `Country` (`wom/models/players/enums.py`)    |
| `player-type.enum.ts`                  | `PlayerType`                                 |
| `player-build.enum.ts`                 | `PlayerBuild`                                |
| `player-status.enum.ts`                | `PlayerStatus`                               |
| `achievement-measure.enum.ts`          | `AchievementMeasure`                         |
| `competition-type.enum.ts`             | `CompetitionType` (`wom/models/competitions/enums.py`) |
| `competition-status.enum.ts`           | `CompetitionStatus`                          |
| `competition-csv-table-type.enum.ts`   | `CompetitionCSVTableType`                    |
| `group-role.enum.ts`                   | `GroupRole` (`wom/models/groups/enums.py`)   |
| `member-activity-type.enum.ts`         | `GroupActivityType`                          |
| `name-change-status.enum.ts`           | `NameChangeStatus` (`wom/models/names/enums.py`) |
| `efficiency-algorithm-type.enum.ts`    | `EfficiencyAlgorithmType` (`wom/models/efficiency/enums.py`) |

List every enum file upstream to spot new ones:

```bash
gh api "repos/wise-old-man/wise-old-man/git/trees/master?recursive=1" --jq '.tree[].path' | grep '^server/src/types/.*\.enum\.ts$'
```

## Adding a metric

`metric.enum.ts` splits metrics into `Skill`, `Activity`, `Boss` and
`ComputedMetric` objects. wom.py mirrors that split:

1. Add the member to `class Metric` in `wom/enums.py`, inside the matching
   comment section (`# Skills`, `# Activities`, `# Bosses`,
   `# Computed Metrics`).
   Place it in the **same position as upstream** (upstream order is mostly
   alphabetical by value). The name is PascalCase, the value is the exact
   upstream string:

   ```py
   TheFracturedArchive = "the_fractured_archive"
   ```

2. Add `Metric.<Name>` to the matching frozenset (`Skills`, `Activities`,
   `Bosses`, or `ComputedMetrics`), in the same relative position.
3. Keep `Unknown = "unknown"` last, under its own `# Unknown` comment.
4. Add a line under `## Additions` in the `# Unreleased` section of
   `CHANGELOG.md` (create the section at the top if it does not exist), in the
   existing style: `- Add support for the <Display Name> boss metric.`
5. `grep -rn "<NeighborMember>" docs tests` to check for hard-coded metric
   lists or counts that need the new member too.

If upstream renames or removes a value, that is a **breaking** change for
wom.py users: stop and confirm with the user before doing it, and note it under
`## Breaking changes` in the CHANGELOG.

## Adding any other enum value

Same idea: PascalCase name, exact upstream string as the value, upstream
position, `Unknown` stays last. `Country` member names capitalize the first
letter of each underscore-separated part of the code (`Ad = "AD"`,
`Gb_Eng = "GB_ENG"`).

A brand-new enum class needs `BaseEnum` as its base, an `Unknown = "unknown"`
member (the `_missing_` fallback relies on it), and entries in the module
`__all__` and the top-level `wom/__init__.py` `__all__` (see
`.claude/rules/conventions.md`).

## Full sync

When asked to sync everything, diff each upstream file in the table against the
wom.py enum by **value**, and report three lists before editing anything:
values missing in wom.py, values in wom.py not upstream (possible removals),
and upstream enum files with no wom.py counterpart. Add the missing ones, and
ask before touching removals.

## Verify and land

1. `nox` (at least `nox -s tests types formatting imports alls`).
2. Follow `.claude/rules/git.md`: branch `feat/<metric-slug>` (or
   `fix/missing-country-values`), commit without a co-author trailer, and only
   open a PR when the user asks for one.
