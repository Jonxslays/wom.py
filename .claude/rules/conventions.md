# Conventions

All of these are enforced by `nox` sessions and will fail CI if violated.

## `__all__` discipline + flat re-export

Every public symbol must be listed in its own module's `__all__` **and**
re-exported at the top level so it is reachable as `wom.<Symbol>`. `wom/__init__.py`
does `from .<module> import *` for each subpackage and then lists every symbol
(and every submodule name) in its own `__all__`.

`scripts/alls.py` (via `nox -s alls`) enforces the two sets match in both
directions: a symbol exported at module level but missing from the top level (or
vice versa) fails. So when you add a model, enum, service, etc., update the
module `__all__` **and** the top-level `wom/__init__.py` `__all__`.

## License header

Every `.py` file under `wom/`, every `.py` in `tests/`, and the root-level
scripts must begin with the two-line MIT header:

```py
# wom.py - An asynchronous wrapper for the Wise Old Man API.
# Copyright (c) 2023-present Jonxslays
```

(followed by the rest of the standard MIT block). `nox -s licensing` checks the
first two lines contain `# wom.py -` and `# Copyright (c)`. Copy the header
verbatim from any existing file when creating a new one.

## Formatting and imports

- **ruff format**, line length **99** (`nox -s formatting`, run as
  `ruff format --check`).
- **ruff check** (`nox -s imports`) enforces import sorting (`I`, with
  `force-single-line = true` — one import per line, no grouped
  `from x import (a, b)`) and the pyflakes import rules (`F4`, unused /
  star-import checks). `F403`/`F405` are ignored for the intentional
  star-imports, and `__init__.py` is exempt from `F401`. Config lives under
  `[tool.ruff]` in `pyproject.toml`.
- Docs prose wraps at **80** columns.

## Docstrings

Google-style docstrings on public classes and methods. They frequently include:

- mkdocs admonitions: `!!! note`, `!!! warning`, `!!! info`, `!!! tip`,
  `??? example` (collapsible), `!!! success` / `!!! failure`.
- Cross-reference links in the form `[Type][wom.Type]` (e.g.
  `[`Client`][wom.Client]`).
- A `Parameters` / `Returns` section, and often a runnable `??? example` code
  block showing client setup.

## Version bumps

Keep `version` in `pyproject.toml` and `__version__` in `wom/__init__.py` in
sync (`scripts/version-check.sh` verifies). Update `CHANGELOG.md` for any
user-facing change.

## Typing / strictness

See `typing.md`: strict mypy + pyright, `from __future__ import annotations`
and `import typing as t` in every module.
