# The Result contract

`Result` (`wom/result.py`) is a Rust-style tagged union with two `@t.final`
variants, `Ok` and `Err`. It is the return type of **every** service method.

## Core rule

**Service methods never raise on API errors.** A failed request produces an
`Err(models.HttpErrorResponse)`, not an exception. Callers must branch on the
result rather than wrapping calls in try/except:

```py
result = await client.players.update_player("Jonxslays")

if result.is_ok:
    print(result.unwrap())        # the model
else:
    print(result.unwrap_err())    # the HttpErrorResponse
```

## API

- `is_ok` / `is_err` — booleans identifying the variant.
- `unwrap()` — returns the value on `Ok`; raises `UnwrapError` on `Err`.
- `unwrap_err()` — returns the error on `Err`; raises `UnwrapError` on `Ok`.
- `to_dict()` — `{"value": ..., "error": None}` for `Ok`, and the mirror for
  `Err` (values converted via `msgspec.to_builtins`).

Unwrapping the wrong variant raises `errors.UnwrapError` (a `WomError`). That is
the intended failure mode for callers who skip the `is_ok` check — do not
suppress it.

## Producing results (inside services)

Do not construct `Ok`/`Err` directly in service methods. Use the `BaseService`
helpers, which return the right variant for you:

- `self._ok_or_err(data, ModelType)` → `Ok(decoded)` when `data` is bytes,
  `Err(data)` when it is already an `HttpErrorResponse`.
- `self._success_or_err(data, predicate=...)` → for bare-success endpoints,
  returns `Ok(HttpSuccessResponse)` or `Err(HttpErrorResponse)`.

`Ok`/`Err` are library-produced only; consumers receive them and should never
need to instantiate them.
