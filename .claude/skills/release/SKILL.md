---
name: release
description: Cut a new wom.py release - bump the version, date the CHANGELOG, open the bump PR, then publish the GitHub release that ships to PyPI. Use when the user says "bump the version", "release X.Y.Z", "cut a release", "deploy", or "publish to PyPI".
---

# Release wom.py

A release has two halves:

1. A **bump PR** that sets the version and dates the CHANGELOG (e.g.
   "Bump version to 3.3.1 (#112)").
2. A **published GitHub release** for tag `vX.Y.Z` on `master`. Publishing it
   triggers `.github/workflows/release.yml`, which runs `scripts/pre-release.sh`,
   builds and uploads to **PyPI**, deploys the **stable docs** with `mike`, and
   posts to the WOM **Discord** webhook.

The second half publishes publicly and can't really be undone (a PyPI version
can never be reused). **Always confirm with the user before creating the
release**, even if they asked for a release at the start.

## 1. Check the starting state

```bash
git fetch origin --tags
git tag -l --sort=v:refname | tail -3
gh release list --limit 3
```

- Releases are sometimes made in the GitHub UI, so always fetch tags before
  trusting local ones.
- Confirm `master` is up to date with `origin/master` and that `CHANGELOG.md`
  starts with a `# Unreleased` section that has content. If there is nothing
  unreleased, stop and tell the user.
- Find the current version in `pyproject.toml`. If a tag for it already
  exists, this is a new version. If the tag does not exist yet, the bump may
  already be merged and only step 4 is left.

## 2. Pick the version

Read the `# Unreleased` section and propose a semver bump:

- **patch**: fixes, new metric or enum values, docs (3.3.0 to 3.3.1 added the
  Fractured Archive metric).
- **minor**: new endpoints, new models or parameters, deprecations.
- **major**: anything under `## Breaking changes`, a dropped Python version, or
  removing deprecated API.

State the proposed version and why, and let the user confirm or override it.

## 3. Bump PR

Branch `chore/bump-version-X.Y.Z` off an up-to-date `master` (see
`.claude/rules/git.md`), then update all of these together:

| File               | Change                                                          |
| ------------------ | --------------------------------------------------------------- |
| `pyproject.toml`   | `version = "X.Y.Z"`                                             |
| `wom/__init__.py`  | `__version__: Final[str] = "X.Y.Z"` (leave `__git_sha__` alone; CI sets it) |
| `uv.lock`          | run `uv lock` so the `wom-py` package entry picks up the version |
| `CHANGELOG.md`     | rename `# Unreleased` to `# vX.Y.Z (Mon YYYY)`, e.g. `# v3.3.1 (Oct 2026)` |

Then:

```bash
./scripts/version-check.sh   # must print vX.Y.Z
nox
```

Commit as `Bump version to X.Y.Z` with no co-author trailer, push the branch,
and open the PR only if the user has asked for it (otherwise stop and offer).
The PR description gets no tool attribution footer.

## 4. Publish the release (after the bump PR is merged)

Confirm with the user first: "Publish vX.Y.Z? This uploads to PyPI, deploys the
stable docs, and posts to Discord." Then:

```bash
git fetch origin --tags
git checkout master && git pull
./scripts/version-check.sh   # must still print vX.Y.Z
```

Release notes are the CHANGELOG section for this version **without** its
`# vX.Y.Z` heading, followed by a full-changelog link:

```text
**Full Changelog**: https://github.com/Jonxslays/wom.py/compare/vPREV...vX.Y.Z
```

Write them to a temp file in the scratchpad, then:

```bash
gh release create vX.Y.Z --target master --title vX.Y.Z --notes-file <notes-file>
```

The user may prefer to click "Publish" in the GitHub UI themselves. If so, hand
them the tag, title and notes instead.

## 5. Verify

```bash
gh run list --workflow release.yml --limit 1
gh run watch <run-id> --exit-status
```

Report the result of both jobs (`pypi` and `docs`). On success, the new version
shows at https://pypi.org/project/wom-py/ and the docs at
https://jonxslays.github.io/wom.py/stable/. If the run fails, show the failing
step's log (`gh run view <run-id> --log-failed`) and do not retry or delete the
release without asking.

## Known gotcha

`scripts/pre-release.sh` finds the latest tag with `git tag -l | tail -1`,
which sorts **alphabetically**. That breaks once a version component reaches
10 (`v3.10.0` sorts before `v3.9.0`), failing the release with "Latest tag
doesn't match project version". If a release is about to hit that, fix the
script first (`git tag -l --sort=v:refname | tail -1`) in its own PR.
