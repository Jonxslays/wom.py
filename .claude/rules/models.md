# Models and enums

## Models

Response models live in `wom/models/<domain>/models.py` and are msgspec
`Struct`s inheriting `BaseModel` (`wom/models/base.py`):

```py
class BaseModel(msgspec.Struct, rename="camel"):
    ...
```

- `rename="camel"` is the key mechanism: it maps the API's **camelCase** JSON
  keys to the model's **snake_case** Python fields automatically. Define fields
  in snake_case; do not hand-write camelCase field names.
- `BaseModel.to_dict()` (via `msgspec.structs.asdict`) is available on every
  model.
- Fields are declared as bare annotations with an **inline docstring** on the
  following line, so mkdocs can render per-field docs:

  ```py
  class Skill(BaseModel):
      """Details regarding a particular skill."""

      metric: enums.Metric
      """The skill being measured."""

      rank: int
      """The players rank in the skill."""
  ```

- Import `BaseModel` from the domain package's relative base (`from ..base
  import BaseModel`); import domain enums from the sibling `.enums`; import
  shared enums from `wom.enums`.

## Enums

Two locations, by scope:

- **Shared enums** used across domains live in the top-level `wom/enums.py`:
  `Metric`, `Period`, `Skills`, `Bosses`, `Activities`, `ComputedMetrics`, plus
  `BaseEnum`.
- **Domain-specific enums** live in `wom/models/<domain>/enums.py` (e.g.
  `PlayerType`, `PlayerBuild`, `Country` under `players`).

All enums inherit `BaseEnum` (from `wom.enums`), which extends `enum.Enum` with
a string `__str__`/`__eq__`. Members are **PascalCase names mapped to the API's
string values**:

```py
class PlayerType(BaseEnum):
    """Different types of players."""

    Unknown = "unknown"
    Regular = "regular"
    FreshStart = "fresh_start"
```

When passing an enum as a request param, send `enum.value` (see
`services-and-endpoints.md`).

## `__all__`

Every model and enum must be listed in its module's `__all__` **and** re-exported
at the top level — see `conventions.md`. Adding one without updating `__all__`
fails `nox -s alls`.
