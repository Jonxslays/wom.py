# Git workflow

**All changes land on a branch and go through a pull request. Never commit
directly to `master`.**

This applies to every change without exception — features, bug fixes, docs,
tests, refactors, chores, and one-line typo fixes alike. `master` is only ever
updated by merging a PR.

## The flow

1. Branch off an up-to-date `master`:

   ```bash
   git checkout master
   git pull
   git checkout -b <type>/<short-description>
   ```

   Use a descriptive prefix: `fix/`, `feat/`, `docs/`, `test/`, `refactor/`,
   `chore/`.

2. Make the change, then run the full quality gate before committing (see
   `CLAUDE.md` / `conventions.md`):

   ```bash
   nox
   ```

3. Commit to the branch (never with a `Co-Authored-By:` trailer — see the
   author's global preference), push, and open a PR against `master`:

   ```bash
   git push -u origin <branch>
   gh pr create --base master
   ```

4. The PR is reviewed and merged into `master`. Delete the branch after merge.

## Rules

- **Never** run `git commit` while `HEAD` is on `master`. If you have already
  staged or committed work on `master` by mistake, move it to a branch before
  pushing (`git branch <name>` then reset `master`), and do not push `master`.
- **Never** `git push` directly to `origin/master`, and never force-push it.
- One logical change per branch/PR. Keep unrelated changes on separate branches.
- Update `CHANGELOG.md` in the same PR for any user-facing change (see
  `conventions.md`).
