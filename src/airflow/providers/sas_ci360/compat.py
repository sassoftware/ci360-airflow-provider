#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

import airflow
from packaging.version import parse as V

AF = V(getattr(airflow, '__version__', '0.0.0'))
IS_V3 = AF >= V('3.0.0')

# ---- Base classes (hooks/operators/triggers)
if IS_V3:
  from airflow.sdk.bases.hook import BaseHook           # type: ignore
  from airflow.sdk.bases.operator import BaseOperator   # type: ignore
else:
  from airflow.hooks.base import BaseHook               # type: ignore
  from airflow.models.baseoperator import BaseOperator  # type: ignore

# ---- get_connection()
if IS_V3:
  from airflow.sdk import Connection
  def get_connection(conn_id: str) -> Connection:
    return Connection.get(conn_id)
else:
  from airflow.models import Connection
  def get_connection(conn_id: str) -> Connection:
    return Connection.get_connection_from_secrets(conn_id)

__all__ = [
  'BaseHook',
  'BaseOperator',
  'get_connection',
  'IS_V3',
  'AF'
]
