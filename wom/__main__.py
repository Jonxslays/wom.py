# wom.py - An asynchronous wrapper for the Wise Old Man API.
# Copyright (c) 2023-present Jonxslays
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Main module entry point, provides version info and exits."""

from __future__ import annotations

import platform
from pathlib import Path

from wom import __git_sha__
from wom import __version__


def _main() -> None:
    """Prints system info and exits."""
    location = Path(__file__).parent.absolute()
    interpreter = platform.python_implementation()
    version = platform.python_version()
    compiler = platform.python_compiler()
    uname = platform.uname()

    metadata = (
        f"Package:     wom.py v{__version__} @ {__git_sha__}",
        f"Location:    {location}",
        f"Interpreter: {interpreter} {version}",
        f"Compiler:    {compiler}",
        f"OS/Arch:     {uname.system} {uname.release} / {uname.machine}",
    )

    separator = "-" * max(len(line) for line in metadata)
    lines = ("\n".join((line, separator)) for line in metadata)
    print("\n".join((separator, *lines)))


if __name__ == "__main__":
    _main()
