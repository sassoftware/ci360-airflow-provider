#!/bin/bash

#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

set -Eeuo pipefail
cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
  echo "ERROR: .venv not found"
  exit 1
fi

source .venv/bin/activate
pip uninstall -y sas_ci360_airflow_provider
