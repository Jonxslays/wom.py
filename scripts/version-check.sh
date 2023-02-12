#!/usr/bin/env sh

PROJECT_VERS=$(grep -m 1 -oP 'version = "(.*)"' pyproject.toml | sed -rn 's/.*"(.*)"/v\1/p');
INIT_VERS=$(sed -rn 's/__version__: Final\[str\] = "(.*)"/v\1/p' wom/__init__.py);

if [ ! "$INIT_VERS" = "$PROJECT_VERS" ]; then
    echo "Project $PROJECT_VERS doesn't match init $INIT_VERS";
    exit 1;
fi

echo $PROJECT_VERS;
