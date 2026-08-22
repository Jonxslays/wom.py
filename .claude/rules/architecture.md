# Architecture

wom.py is an async Python wrapper for the Wise Old Man API. It exposes one
service method per API endpoint and a typed model class for every response.

## Data flow

Every API call flows through the same layers:

```
Client → Service → Route → HttpService → Serializer → Result
```

Each layer owns exactly one job:

- **`Client`** (`wom/client.py`) — the entry point. Owns a single `HttpService`
  and a single `Serializer`, and exposes one service per API domain as a
  property: `.players`, `.groups`, `.competitions`, `.deltas`, `.records`,
  `.names`, `.efficiency`. Services are constructed once in
  `__init_core_services` and share the client's `HttpService`/`Serializer`.
  Also exposes mutators that delegate to the http service: `set_api_key`,
  `unset_api_key`, `set_user_agent`, `set_api_base_url`.

- **Services** (`wom/services/*.py`) — one class per domain, all inheriting
  `BaseService`. Each public method maps to exactly one endpoint. See
  `services-and-endpoints.md`.

- **Routes** (`wom/routes.py`) — module-level `Route("METHOD", "/uri/{}")`
  constants, typed `t.Final[Route]`. `.compile(*args)` substitutes each `{}`
  placeholder positionally (returning a `CompiledRoute`); `.with_params(dict)`
  adds query params and returns the route for chaining.

- **`HttpService`** (`wom/services/http.py`) — owns the aiohttp session, builds
  headers (user agent + optional api key), and performs the request. Turns
  non-OK responses into `models.HttpErrorResponse`. Uses msgspec for
  encode/decode.

- **`Serializer`** (`wom/serializer.py`) — lazily builds and caches one msgspec
  `Decoder` per model type in a dict, keyed on the model type. `decode(data,
  model_type)` fetches/creates the decoder and decodes the bytes.

- **Models** (`wom/models/<domain>/models.py`) — msgspec `Struct`s inheriting
  `BaseModel`. See `models.md`.

- **`Result`** (`wom/result.py`) — a Rust-style `Ok`/`Err` return type. Every
  service method returns a `Result`; API errors never raise. See `results.md`.

## Client lifecycle

- `client = wom.Client(api_key=None, *, user_agent=None, api_base_url=None)` —
  none of the args are required; a user agent is strongly encouraged.
- `await client.start()` **must** be called before any request. It initializes
  the aiohttp session; omitting it crashes with a `RuntimeError`.
- `await client.close()` when done. Safe to call even if the client was never
  started (it no-ops).

## Package surface

Everything is re-exported flat from the top-level `wom` package
(`wom/__init__.py`), so consumers use `wom.Client`, `wom.Metric`,
`wom.PlayerDetail`, etc. — never the deep module path. See `conventions.md` for
the `__all__` / re-export discipline that keeps this surface consistent.
