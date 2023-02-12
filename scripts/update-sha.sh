#!/usr/bin/env sh

echo "Updating git sha to $1...";

sed -i 's/__git_sha__: Final\[str\] = "\[.*\]"/__git_sha__: Final\[str\] = "\['$1'\]"/' \
    wom/__init__.py;
