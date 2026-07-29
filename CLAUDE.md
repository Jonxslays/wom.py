# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

wom.py is an asynchronous Python wrapper for the [Wise Old Man API](https://docs.wiseoldman.net/)
(an Old School RuneScape player progress tracker). It provides one service method per API endpoint
and typed model classes for every response. Python 3.10+, managed with Poetry.

## Commands

Dependencies are managed with Poetry (`poetry install` installs dev deps too). Tasks run through
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
poetry run pytest tests/services/test_records.py -k leaderboard --testdox
```

Docs are built with mkdocs (`poetry run mkdocs serve`).

## Architecture

The data flow for any API call is: **Client → Service → Route → HttpService → Serializer → Result**.

- **[`Client`](wom/client.py)** is the entry point. It owns a single `HttpService` and `Serializer`,
  and exposes one service per API domain as a property (`.players`, `.groups`, `.competitions`,
  `.deltas`, `.records`, `.names`, `.efficiency`). `await client.start()` must be called before any
  request (it initializes the aiohttp session — omitting it raises `RuntimeError`); `await client.close()`
  when done.

- **Services** (`wom/services/*.py`) all inherit [`BaseService`](wom/services/base.py). Each public
  method maps to exactly one endpoint. The pattern is: build a params dict with `self._generate_map(...)`
  (drops `None` values), compile a `Route`, `await self._http.fetch(route)`, then wrap the bytes in a
  `Result` via `self._ok_or_err(data, ModelType)`. `_success_or_err` handles endpoints that return a
  bare success message instead of a model.

- **[Routes](wom/routes.py)** are declared as module-level `Route("METHOD", "/uri/{}")` constants.
  `.compile(*args)` substitutes `{}` placeholders positionally; `.with_params(dict)` adds query params.

- **[`HttpService`](wom/services/http.py)** handles the aiohttp session, headers (user agent + optional
  api key), and turns non-OK responses into `models.HttpErrorResponse`. Uses msgspec for encode/decode.

- **[`Serializer`](wom/serializer.py)** lazily builds and caches one msgspec `Decoder` per model type.

- **Models** (`wom/models/<domain>/models.py`) are msgspec `Struct`s inheriting
  [`BaseModel`](wom/models/base.py), which sets `rename="camel"` — this is how the API's camelCase JSON
  maps to the snake_case Python fields. Each domain also has an `enums.py`. Shared enums (e.g. `Metric`,
  `Period`) live in the top-level [`wom/enums.py`](wom/enums.py).

- **[`Result`](wom/result.py)** is a Rust-style `Ok`/`Err` type. **Every service method returns a
  `Result`, never raises on API errors.** Callers check `result.is_ok` then `result.unwrap()` /
  `result.unwrap_err()` (unwrapping the wrong variant raises `UnwrapError`).

Everything is re-exported flat from the top-level `wom` package (`wom/__init__.py`), so public symbols
are used as `wom.Client`, `wom.Metric`, etc.

## Conventions

- **`__all__` discipline:** every public symbol must be listed in its module's `__all__` AND re-exported
  at the top level. `scripts/alls.py` (via `nox -s alls`) enforces this — adding a model/enum without
  updating `__all__` will fail CI.
- **License header:** every `.py` file (including tests and root scripts) must begin with the two-line
  `# wom.py -` / `# Copyright (c)` header. Enforced by `nox -s licensing`.
- **Strict typing:** both mypy and pyright run in strict mode. Code uses `from __future__ import
  annotations` everywhere and `import typing as t`.
- **Style:** black (line length 99), isort with `force_single_line = true` (one import per line).
  Docs line length is 80. Docstrings are Google-style and often include mkdocs admonitions and
  `[Type][wom.Type]` cross-reference links.
- **Version bumps:** keep `version` in [pyproject.toml](pyproject.toml) and `__version__` in
  `wom/__init__.py` in sync (`scripts/version-check.sh` verifies this). Update [CHANGELOG.md](CHANGELOG.md).

## Adding a new endpoint

1. Add a `Route` constant in [wom/routes.py](wom/routes.py).
2. Add any new response models to the relevant `wom/models/<domain>/models.py` (and enums), updating
   every `__all__` up the chain.
3. Add the service method to the matching `wom/services/<domain>.py`, returning a `ResultT[...]`.
4. Add tests under `tests/` and run `nox`.
