# Contributing

Thanks for your interest in wom.py! Here are some tips for contributing.

## Guidelines

- If you have an idea, but are unsure on the proper implementation - open an issue.
- Implementations should be well tested before opening a pull request.
- Max code line length of 99, max docs line length of 80.
- Code should be written in [black](https://github.com/psf/black)'s code style.
- Code should be [PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.
- Use informative commit messages.

## Installing poetry

wom.py uses [Poetry](https://python-poetry.org/) for dependency management.

Check out poetry's full
[installation guide](https://python-poetry.org/docs/#installation)
for detailed instructions if you aren't familiar with it.

## Installing dependencies

1. Create a fork of wom.py, and clone the fork to your local machine.
2. Change directory into the project dir.
3. Run `poetry shell` to create a new virtual environment, and activate it.
4. Run `poetry install` to install dependencies (this includes dev deps).

## Writing code

1. Check out a new branch to commit your work to, e.g. `git checkout -b bugfix/typing-errors`.
2. Make your changes, then run `nox` and address any issues that arise.
3. Commit your work, using an informative commit message.
4. Open a pull request into the master branch of this repository.

After submitting your PR, it will be reviewed (and hopefully merged!).
Thanks again for taking the time to read this contributing guide, and for your
interest in wom.py. I look forward to working with you.
