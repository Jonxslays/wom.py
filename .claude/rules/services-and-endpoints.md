# Services and endpoints

Each domain has one service class in `wom/services/<domain>.py`, all inheriting
`BaseService` (`wom/services/base.py`). Every public method maps to **exactly
one** API endpoint and returns a `ResultT[...]` (see `results.md`).

## The per-endpoint method pattern

The canonical shape (from `wom/services/players.py`):

```py
async def get_details(self, username: str) -> ResultT[models.PlayerDetail]:
    """<Google-style docstring with an ??? example block and Parameters.>"""
    route = routes.PLAYER_DETAILS.compile(username)
    data = await self._http.fetch(route)
    return self._ok_or_err(data, models.PlayerDetail)
```

With query params:

```py
params = self._generate_map(username=username, limit=limit, offset=offset)
route = routes.SEARCH_PLAYERS.compile().with_params(params)
data = await self._http.fetch(route)
return self._ok_or_err(data, t.List[models.Player])
```

Steps, in order:

1. **Build the params map** with `self._generate_map(**kwargs)` — it drops any
   key whose value is `None`, so you pass every optional straight through.
2. **Convert non-primitive params** as you put them in the map:
   - enums → `some_enum.value` (e.g. `period=period.value if period else None`),
   - datetimes → `.isoformat()` (e.g. `startDate=start_date.isoformat() if
     start_date else None`).
   - Note query-param keys use the API's spelling (`startDate`, `endDate`) when
     passed directly to `_generate_map`.
3. **Compile the route**: `routes.SOME_ROUTE.compile(*uri_args)`, then
   `.with_params(params)` if there are query params. `.compile()` /
   `.with_params()` may be chained either inline or across two statements — both
   styles exist in the codebase.
4. **Fetch**: `data = await self._http.fetch(route)`.
5. **Wrap the result**:
   - `self._ok_or_err(data, ModelType)` for endpoints returning a model. Pass a
     parameterized type for lists: `self._ok_or_err(data, t.List[models.X])`.
   - `self._success_or_err(data)` for endpoints that return a bare success
     message (`HttpSuccessResponse`) instead of a model. Accepts an optional
     `predicate` callable to decide success from the message string; the default
     predicate checks `message.startswith("Success")`.

`BaseService` helpers you build on: `_generate_map`, `_ok`, `_ok_or_err`,
`_success_or_err`. Do not call `self._http` or the serializer with raw error
handling in a method — go through these helpers so the `Ok`/`Err` contract stays
uniform.

Service classes set `__slots__ = ()` (fields live on `BaseService`).

## Adding a new endpoint (checklist)

1. Add a `Route` constant in `wom/routes.py`
   (`NAME: t.Final[Route] = Route("METHOD", "/uri/{}")`).
2. Add any new response models to the relevant `wom/models/<domain>/models.py`
   (and enums to that domain's `enums.py`), updating every `__all__` up the
   chain — see `models.md` and `conventions.md`.
3. Add the service method to the matching `wom/services/<domain>.py`, following
   the pattern above and returning a `ResultT[...]`.
4. Add tests under `tests/` and run `nox`.
