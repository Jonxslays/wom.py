# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

wom.py is an asynchronous Python wrapper for the [Wise Old Man API](https://docs.wiseoldman.net/)
(an Old School RuneScape player progress tracker). It provides one service method per API endpoint
and typed model classes for every response. Python 3.10+, managed with uv.

## Commands

Dependencies are managed with uv (`uv sync` installs dev deps too). Tasks run through
[nox](noxfile.py) — each session installs its own pinned deps into a reused venv:

```bash
nox                 # run all sessions (tests, types, formatting, imports, licensing, alls)
nox -s tests        # pytest with coverage + testdox output
nox -s coverage     # print coverage report (requires a prior tests run producing .coverage)
nox -s types        # mypy + pyright, both in strict mode
nox -s formatting   # black --check (line length 99)
nox -s imports      # isort check + flake8 (unused/star-import checks only, F4)
nox -s licensing    # verify every .py file has the MIT license header
nox -s alls         # runs scripts/alls.py to verify __all__ exports are consistent
```

Run a single test with pytest directly (asyncio_mode is `auto`, so no decorator needed):

```bash
uv run pytest tests/services/test_records.py -k leaderboard --testdox
```

Docs are built with mkdocs (`uv run mkdocs serve`).

## Coding conventions and architecture

Detailed, dedicated rules for how code is written in this repo live in
[`.claude/rules/`](.claude/rules/). Read the relevant file before making changes:

- **[architecture.md](.claude/rules/architecture.md)** — the
  `Client → Service → Route → HttpService → Serializer → Result` data flow, what
  each layer owns, and the `start()`/`close()` client lifecycle.
- **[services-and-endpoints.md](.claude/rules/services-and-endpoints.md)** — the
  per-endpoint method pattern (`_generate_map`, compile a `Route`, `_http.fetch`,
  `_ok_or_err` / `_success_or_err`) and the step-by-step checklist for adding a
  new endpoint.
- **[results.md](.claude/rules/results.md)** — the `Ok`/`Err` `Result` contract:
  every service method returns a `Result` and never raises on API errors.
- **[models.md](.claude/rules/models.md)** — msgspec `Struct` models, `BaseModel`
  `rename="camel"` camelCase↔snake_case mapping, and where enums live (domain
  `enums.py` vs top-level `wom/enums.py`).
- **[typing.md](.claude/rules/typing.md)** — strict mypy + pyright,
  `from __future__ import annotations`, `import typing as t`, and `ResultT`
  return types.
- **[conventions.md](.claude/rules/conventions.md)** — `__all__` discipline and
  flat top-level re-export, the MIT license header, black/isort style,
  Google-style docstrings, and version-bump syncing.
