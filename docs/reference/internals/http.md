# HTTP

The internal service that owns the `aiohttp` session and performs every
request, and the base class the public services inherit from. The
[`Client`][wom.Client] creates and owns these; you should not need to use them
directly.

::: wom.services.HttpService
    options:
      show_root_heading: true

::: wom.services.BaseService
    options:
      show_root_heading: true
