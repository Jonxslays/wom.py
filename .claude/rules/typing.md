# Typing

Both **mypy and pyright run in strict mode** (`nox -s types` runs both). Public
APIs must be fully typed; there are no untyped escape hatches.

## Required in every module

- `from __future__ import annotations` — the first import in every `.py` file,
  right under the license header.
- `import typing as t` — typing is always aliased to `t` and referenced as
  `t.Optional`, `t.List`, `t.Dict`, `t.Union`, `t.Type`, `t.Any`, `t.TypeVar`,
  etc. (`from typing import Final` and similar direct imports appear only in a
  few module-header spots like `wom/__init__.py`; prefer `t.` in new code.)

## Return types

Service methods return a `Result`, aliased per service module as:

```py
T = t.TypeVar("T")
ResultT = result.Result[T, models.HttpErrorResponse]
```

So a method annotates its return as `ResultT[models.PlayerDetail]` or
`ResultT[t.List[models.Player]]`. `BaseService` declares the same alias under
`if t.TYPE_CHECKING:` for internal helpers.

## Conventions

- Keyword-only options use `*` in the signature and are `t.Optional[...] =
  None` (e.g. `*, limit: t.Optional[int] = None, offset: t.Optional[int] =
  None`).
- Runtime-only-optional imports and type aliases go under
  `if t.TYPE_CHECKING:  # pragma: no cover`.
- Narrow, targeted ignores only, with the tool named:
  `# type: ignore[...]` (mypy) and `# pyright: ignore[...]` (pyright). Never a
  bare blanket ignore.
- `t.final` marks classes not meant to be subclassed (e.g. `Ok`, `Err`).
- Classes define `__slots__` (often `()` on subclasses that add no fields).
- Route constants are annotated `t.Final[Route]`.
