# errors

Exception types raised by the library. Note that API errors do **not** raise -
they come back as an [`Err`][wom.Err]; these exceptions cover misuse such as
unwrapping the wrong [`Result`][wom.Result] variant.

::: wom.errors
