# The result type

Those of you familiar with [Rust](https://www.rust-lang.org/) will feel right at
home with the [`Result`][wom.Result] type this library implements. All requests
that go out over the network via the [`Client`][wom.Client] come back to you in
the form of a [`Result`][wom.Result]. The result can be one of two things:
an [`Ok`][wom.Ok] or an [`Err`][wom.Err].

!!! info

    Service methods **never raise** on an API error. A failed request comes back
    as an [`Err`][wom.Err] wrapping an
    [`HttpErrorResponse`][wom.HttpErrorResponse], so you branch on the result
    instead of wrapping calls in `try`/`except`.

## The API

- [`is_ok`][wom.Result.is_ok] / [`is_err`][wom.Result.is_err] - booleans
  identifying the variant.
- [`unwrap()`][wom.Result.unwrap] - returns the value on an [`Ok`][wom.Ok];
  raises [`UnwrapError`][wom.UnwrapError] on an [`Err`][wom.Err].
- [`unwrap_err()`][wom.Result.unwrap_err] - returns the error on an
  [`Err`][wom.Err]; raises [`UnwrapError`][wom.UnwrapError] on an [`Ok`][wom.Ok].
- [`to_dict()`][wom.Result.to_dict] - `{"value": ..., "error": None}` for an
  [`Ok`][wom.Ok], and the mirror for an [`Err`][wom.Err].

Always check [`is_ok`][wom.Result.is_ok] (or [`is_err`][wom.Result.is_err])
before unwrapping, so you unwrap the variant you actually have.

## Correct usage

```py
client = wom.Client(user_agent="@jonxslays")

await client.start()

result = await client.players.update_player("jonxslays")

if result.is_ok:
    print(result.unwrap())
else:
    print(result.unwrap_err())

await client.close()
```

## Incorrect usage

```py
client = wom.Client(user_agent="@jonxslays")

await client.start()

result = await client.players.update_player("eeeeeeeeeeeee")

print(result.unwrap()) # <-- Exception raised
# Raises UnwrapError because username should have been 12 characters or less

# .. Remember to close the client!
```
