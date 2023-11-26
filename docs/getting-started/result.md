# The result type

Those of you familiar with [Rust](https://www.rust-lang.org/) will feel right at
home with the [`Result`][wom.Result] type this library implements. All requests
that go out over the network via the [`Client`][wom.Client] come back to you in
the form of a [`Result`][wom.Result]. The result can be one of two things:
an [`Ok`][wom.Ok] or an [`Err`][wom.Err].

Calling [`unwrap()`][wom.Result.unwrap] on an [`Err`][wom.Err] will raise an
exception.

Calling [`unwrap_err()`][wom.Result.unwrap_err] on an [`Ok`][wom.Ok] will raise
an exception.

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
