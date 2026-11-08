# Handling errors

wom.py separates **API errors**, which come back as values, from **library
misuse and network failures**, which raise exceptions. Knowing which is which
tells you where you need an `if` and where you need a `try`.

## API errors are values

Service methods never raise when the API rejects a request. Instead they return
an [`Err`][wom.Err] wrapping an [`HttpErrorResponse`][wom.HttpErrorResponse]:

| Field | Type | Description |
| --- | --- | --- |
| `message` | `str` | The human readable error message from the API. |
| `status` | `int` | The HTTP status code, for example `404`. |
| `code` | `str \| None` | A machine readable error code, when the API sends one. |

```py
result = await client.players.get_details("not a real player")

if result.is_err:
    error = result.unwrap_err()
    print(error.status)   # 404
    print(error.message)  # Player not found
    print(error.code)     # PLAYER_NOT_FOUND
```

See [the result type](../getting-started/result.md) for the full
[`Result`][wom.Result] API.

## Branching on the status code

The WOM API uses conventional HTTP status codes, so `status` is usually the
most useful thing to branch on:

| Status | Meaning |
| --- | --- |
| `400` | Bad request, for example an invalid username or conflicting params. |
| `403` | Forbidden, usually a wrong or missing verification code. |
| `404` | The player, group, competition, or name change doesn't exist. |
| `429` | Too many requests. You hit a rate limit, or updated a player too often. |
| `500` | Something went wrong on the WOM servers. |

```py
result = await client.players.get_details("Jonxslays")

if result.is_ok:
    player = result.unwrap()
    print(f"{player.display_name} is level {player.combat_level}")
else:
    error = result.unwrap_err()

    if error.status == 404:
        print("WOM isn't tracking that player yet.")
    elif error.status == 429:
        print("Slow down! Try again in a minute.")
    else:
        print(f"Request failed ({error.status}): {error.message}")
```

!!! tip

    Prefer `status` (or `code`, when present) over matching on `message`. The
    message text is meant for humans and may change without notice.

Rate limits are covered in more detail in
[requests and rate limits](requests.md#rate-limits).

## Bare message endpoints

Some endpoints, like deleting a group or adding competition participants, don't
return a model. They return an [`Ok`][wom.Ok] wrapping an
[`HttpSuccessResponse`][wom.HttpSuccessResponse] with the API's success message
instead, and an [`Err`][wom.Err] on failure as usual:

```py
result = await client.groups.delete_group(123, "111-111-111")

if result.is_ok:
    print(result.unwrap().message)  # The API's confirmation message
```

## What does raise

A few things raise exceptions instead of returning an [`Err`][wom.Err]. They
all indicate a bug in your code or a problem outside the API itself:

- [`UnwrapError`][wom.UnwrapError] - calling
  [`unwrap()`][wom.Result.unwrap] on an [`Err`][wom.Err], or
  [`unwrap_err()`][wom.Result.unwrap_err] on an [`Ok`][wom.Ok]. Check
  [`is_ok`][wom.Result.is_ok] first.
- `RuntimeError` - making a request before calling
  [`Client.start`][wom.Client.start].
- `TypeError` - calling a method with arguments it can't accept, for example
  [`create_competition`][wom.CompetitionService.create_competition] without
  `starts_at` and `ends_at`.
- `aiohttp` exceptions such as `aiohttp.ClientConnectionError` or
  `asyncio.TimeoutError` - the request never reached the API (no network, DNS
  failure, timeout). wom.py doesn't swallow these, so wrap your calls if your
  application needs to survive network outages:

```py
import aiohttp

try:
    result = await client.players.get_details("Jonxslays")
except aiohttp.ClientError as e:
    print(f"Couldn't reach the WOM API: {e}")
else:
    ...  # Branch on the result as usual
```

All exceptions defined by wom.py inherit from [`WomError`][wom.WomError].

## Unknown enum values

When the API sends an enum value wom.py doesn't know about yet (for example a
brand new boss), it is decoded as that enum's `Unknown` variant and an
[`UnknownEnumWarning`][wom.UnknownEnumWarning] is emitted, rather than failing
the whole request. Upgrading wom.py usually adds the new value. See
[metrics and enums](metrics.md#unknown-values) for details.
