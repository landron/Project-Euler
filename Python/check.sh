#!/bin/bash

# pip install ./lang
# pip install ./lang --upgrade # it seems unneeded

set -euo pipefail
# set -x

# fmt: off/on
black ./
flake8 ./
# pylint ./

for f in lang/src/project_euler/*.py; do
  [[ $(basename "$f") == "__init__.py" ]] && continue
#   echo "Executing $f"
  python "$f"
done
