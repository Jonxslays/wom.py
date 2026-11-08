# Contributing

Thanks for your interest in wom.py! This guide covers how to set up the
project, the checks your change needs to pass, and checklists for the most
common kinds of contribution.

If you have an idea but are unsure how to implement it, or want to check it's
wanted before you start, [open an issue](https://github.com/Jonxslays/wom.py/issues/new/choose)
first.

## Setting up

wom.py uses [uv](https://docs.astral.sh/uv/) for dependency management. See
uv's [installation guide](https://docs.astral.sh/uv/getting-started/installation/)
if you don't have it yet.

1. Fork wom.py and clone your fork.
2. `cd` into the project directory.
3. Run `uv sync` to create a virtual environment and install all dependencies,
   including the dev tools.
4. Prefix commands with `uv run` (for example `uv run nox`) to run them in that
   environment, or activate `.venv` directly.

## Making a change

1. Create a branch for your work, using a prefix that describes it:
   `fix/`, `feat/`, `docs/`, `test/`, `refactor/`, or `chore/`. For example
   `git checkout -b fix/typing-errors`.
2. Make your changes, adding or updating tests for any behavior change.
3. Update `CHANGELOG.md` if the change is user-facing (see
   [the changelog](#the-changelog)).
4. Run `uv run nox` and fix anything it reports.
5. Commit with an informative message, push, and open a pull request against
   `master`. Keep each pull request to one logical change.

After you open your PR it will be reviewed, and hopefully merged!

## Checks

Everything CI checks can be run locally through [nox](https://nox.thea.codes/).
Running `uv run nox` with no arguments runs every session:

| Command | What it checks |
| --- | --- |
| `uv run nox -s tests` | The test suite, with coverage. |
| `uv run nox -s types` | mypy and pyright, both in strict mode. |
| `uv run nox -s formatting` | Code is formatted with `ruff format`. |
| `uv run nox -s imports` | Import sorting and unused imports, with `ruff check`. |
| `uv run nox -s licensing` | Every `.py` file starts with the license header. |
| `uv run nox -s alls` | `__all__` exports are consistent (see below). |
| `uv run nox -s docs` | The docs build with no warnings or broken links. |

To run a single test file or test while you work, use pytest directly:

```sh
uv run pytest tests/services/test_records.py -k leaderboard --testdox
```

Tests are async-aware (`asyncio_mode = "auto"`), so `async def` tests need no
decorator.

## Code style

Most style rules are enforced by the checks above, but a few are easiest to get
right from the start:

- **Formatting.** Run `uv run ruff format .` before committing. The max line
  length is 99 for code and 80 for docs prose.
- **Imports.** One import per line (`from x import a` and `from x import b`
  separately, not `from x import a, b`). `uv run ruff check --fix wom tests`
  sorts them for you.
- **Typing.** Every module starts with `from __future__ import annotations` and
  imports typing as `import typing as t`. Public APIs must be fully typed, and
  any type-checker ignore must be narrow and name the tool, like
  `# type: ignore[attr-defined]` or `# pyright: ignore[reportPrivateUsage]`.
- **License header.** Every new `.py` file must start with the MIT license
  header. Copy it verbatim from any existing file.
- **Exports.** Every public symbol goes in its module's `__all__` **and** in
  the top-level `wom/__init__.py` `__all__`, so users can always write
  `wom.MySymbol`. `nox -s alls` fails if the two disagree.
- **Docstrings.** Public classes and methods use
  [NumPy-style](https://numpydoc.readthedocs.io/en/latest/format.html)
  docstrings with `Parameters` and `Returns` sections. Service methods
  include a `??? example` block. Link to other symbols with
  `` [`Name`][wom.Name] ``.
- **Results, not exceptions.** Service methods return a `Result` and never
  raise on API errors. Use the `BaseService` helpers (`_ok_or_err`,
  `_success_or_err`) rather than building `Ok`/`Err` yourself.

## Common contributions

### Adding a new endpoint

1. Add a `Route` constant to `wom/routes.py`:
   `NAME: t.Final[Route] = Route("GET", "/uri/{}")`.
2. Add any new response models to `wom/models/<domain>/models.py` as `msgspec`
   structs inheriting `BaseModel`, with snake_case fields (the camelCase JSON
   keys are mapped automatically). New enums go in that domain's `enums.py`.
3. Add the method to the matching service in `wom/services/<domain>.py`,
   following the pattern of the existing methods: build params with
   `self._generate_map(...)`, compile the route,
   `await self._http.fetch(route)`, and return
   `self._ok_or_err(data, models.YourModel)`.
4. Export every new symbol (see **Exports** above).
5. Add tests under `tests/`, and add the method to the table in
   `docs/getting-started/endpoints.md`.

### Adding a metric or enum value

When WOM adds a new boss, skill, activity, or other enum value:

1. Add the member to the right enum. Metrics go in `class Metric` in
   `wom/enums.py`, inside the matching section (`# Skills`, `# Activities`,
   `# Bosses`, `# Computed Metrics`), in the same position as the
   [upstream enum](https://github.com/wise-old-man/wise-old-man/tree/master/server/src/types).
   The name is PascalCase and the value is the exact upstream string, for
   example `TheFracturedArchive = "the_fractured_archive"`.
2. For metrics, also add it to the matching frozenset (`Skills`, `Bosses`,
   `Activities`, or `ComputedMetrics`).
3. Keep the `Unknown` member last.
4. Add a CHANGELOG entry, such as
   `- Add support for the <Display Name> boss metric.`

### Improving the docs

The docs are built with [MkDocs](https://www.mkdocs.org/). The API reference
is generated from docstrings, and the guides live in `docs/` as Markdown.

- `uv run mkdocs serve` serves the docs locally with live reload at
  <http://127.0.0.1:8000>.
- `uv run nox -s docs` builds them in strict mode, which fails on broken
  cross-references. Run it before opening a docs PR.

## The changelog

Add an entry under the `# Unreleased` section at the top of `CHANGELOG.md` for
any change users would notice: new features, bug fixes, deprecations, and
breaking changes. Create the section if it doesn't exist yet, and group entries
under headings like `## Additions`, `## Changes`, `## Bug fixes`,
`## Deprecations`, and `## Breaking changes`. Internal-only changes like test
refactors don't need an entry.

The maintainer handles version bumps and releases, so don't change the version
in your PR.

---

Thanks again for taking the time to read this guide, and for your interest in
wom.py. I look forward to working with you!
