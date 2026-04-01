#!/bin/bash

set -euo pipefail
cd "$(dirname "$0")/.."

dump() {
  f="$1"
  echo "===== ${f} ====="
  cat "$f"
  echo
}

dump "pyproject.toml"
dump ".github/workflows/release.yml"

shopt -s globstar nullglob
for f in src/**/*.py; do
  dump "$f"
done

dump "samples/ci360_airflow.py"
