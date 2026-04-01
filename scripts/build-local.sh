#!/bin/bash

#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

set -Eeuo pipefail
cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
  echo "ERROR: .venv not found"
  exit 1
fi

rm -rf dist/ build/ *.egg-info

source .venv/bin/activate
python -m build

pip install dist/*.whl --upgrade
