---
name: api-drift
description: Audit wom.py against the upstream Wise Old Man API for drift - missing or removed endpoints, changed response shapes, new or deprecated query params and request fields, and new enum values. Use when the user asks "what's changed upstream", "check for API drift", "are we missing any endpoints", or before planning a release.
---

# API drift audit

Upstream is the `wise-old-man/wise-old-man` repo, branch `master`. Everything
here is read-only until the user picks what to act on. The output is a
report, and, if the user wants, GitHub issues in the style of #114 (summary,
upstream PR links, API shape changes, task checklist).

## 1. Routes

```bash
sh .claude/skills/api-drift/route-diff.sh          # against upstream master
sh .claude/skills/api-drift/route-diff.sh <sha>    # against a specific ref
```

The script normalizes path params (`:username` to `{}`) and prints routes only
upstream has and routes only wom.py has (`wom/routes.py`).

For each **upstream-only** route, open its router file
(`server/src/api/modules/<domain>/<domain>.router.ts`) and check whether
`checkAdminPermission` is the first middleware after the path. Admin-gated
routes need the WOM master key and are intentionally **left out** of wom.py.
Some routes only gate part of their behavior (for example `POST
/players/:username` checks admin only when `force` is set), and those count as
public.

As of 2026-11-07 all 20 upstream-only routes were admin-gated: player
delete/rollback/rollback-snapshot-metric-values/archive/country/annotation (add
and delete), name-change approve/deny/clear-history, group and competition
reset-code and visibility, group verify, api-key create and revoke, block and
allow actions, and patron claim. Only report routes outside that set as new,
unless one of these lost its admin gate.

Any **wom.py-only** route means upstream removed or renamed it. That's
breaking for users, so flag it prominently.

## 2. What changed since the last audit

Find recent upstream API commits, and use the last audit date if the user's
memory has one:

```bash
gh api "repos/wise-old-man/wise-old-man/commits?path=server/src/api&since=<YYYY-MM-DDT00:00:00Z>&per_page=100" \
  --jq '.[] | "\(.sha[0:7]) \(.commit.author.date[0:10]) \(.commit.message | split("\n")[0])"'
```

Skim the `[server]` / `[api]` commits and their PRs
(`gh pr view <n> --repo wise-old-man/wise-old-man --json title,body,files`).
PR bodies often say outright what changed in the response or request shape
(that's how the multi-metric competitions change, #1762, was found).

## 3. Response shapes

Response types live in `server/src/api/responses/*.response.ts`. Each
`format...Response` function shows exactly which fields go out. Compare the
fields with the matching msgspec model in `wom/models/<domain>/models.py`,
remembering that `BaseModel` maps camelCase to snake_case:

- A **new upstream field** missing from the model is silently dropped on
  decode. It's additive, so add it, with a default if older payloads lack it.
- A **removed or renamed upstream field** that the model requires with no
  default makes decoding fail for every call that returns it. That's urgent.
- **Type changes** (for example `Metric` to `Metric | 'total'`, or int to
  float) can fail decoding too.

Read only the responses touched by commits from step 2, unless the user asked
for a full audit.

## 4. Params and bodies

In the router, each route's `validateRequest({ query, body })` zod schema is
the contract. Look for:

- New optional query params or body fields that the wom.py service method
  doesn't accept yet.
- Fields marked `@deprecated` (upstream keeps the old name as an alias for a
  while), so wom.py can add the replacement and deprecate its own.
- New error codes in the route's `switch` (for example
  `METRICS_MUST_BE_OF_SAME_TYPE`). These come back as a normal `Err`, so they
  usually only need a test or a docs note.

## 5. Enums

Run the **sync-enums** skill's full sync and include its three lists in the
report.

## Report

Group findings by urgency:

1. **Breaking or decode failures**: removed routes, removed or renamed
   required fields, type changes.
2. **New public features**: new routes, new fields, new params, new enum
   values.
3. **Deprecations**: upstream aliases to migrate to.
4. **Ignored**: admin-gated routes (just list them).

Cite upstream PR numbers as `wise-old-man/wise-old-man#<n>`. Offer to open one
issue per logical change and, after writing them, update the
`api-drift-public-gaps` memory with the audit date and the admin-gated count.
