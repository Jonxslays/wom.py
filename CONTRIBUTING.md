# Contributing

Thanks for your interest in wom.py! Here are some tips for contributing.

## Guidelines

- If you have an idea, but are unsure on the proper implementation - open an issue.
- Implementations should be well tested before opening a pull request.
- Max code line length of 99, max docs line length of 80.
- Code should be formatted with [ruff](https://docs.astral.sh/ruff/) (`ruff format`);
  imports and lint checks are also enforced by `ruff check`.
- Code should be [PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.
- Use informative commit messages.

## Installing uv

wom.py uses [uv](https://docs.astral.sh/uv/) for dependency management.

Check out uv's full
[installation guide](https://docs.astral.sh/uv/getting-started/installation/)
for detailed instructions if you aren't familiar with it.

## Installing dependencies

1. Create a fork of wom.py, and clone the fork to your local machine.
2. Change directory into the project dir.
3. Run `uv sync` to create a virtual environment and install dependencies
   (this includes dev deps).
4. Prefix commands with `uv run` (e.g. `uv run nox`) to run them inside the
   managed environment, or activate `.venv` directly.

## Writing code

1. Check out a new branch to commit your work to, e.g. `git checkout -b bugfix/typing-errors`.
2. Make your changes, then run `uv run nox` and address any issues that arise.
3. Commit your work, using an informative commit message.
4. Open a pull request into the master branch of this repository.

After submitting your PR, it will be reviewed (and hopefully merged!).
Thanks again for taking the time to read this contributing guide, and for your
interest in wom.py. I look forward to working with you.
