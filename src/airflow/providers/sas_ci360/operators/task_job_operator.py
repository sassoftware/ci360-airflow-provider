#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict
from airflow.providers.sas_ci360 import constants
from airflow.providers.sas_ci360.client import CI360Client
from airflow.providers.sas_ci360.models import CI360TaskJob
from airflow.providers.sas_ci360.triggers import CI360TaskJobTrigger
from .job_operator import CI360JobOperator

if TYPE_CHECKING:
  from airflow.utils.context import Context

class CI360TaskJobOperator(CI360JobOperator):
  '''Execute a CI 360 task, defer until completion'''

  custom_operator_name = constants.TASK_UI_LABEL
  ui_fgcolor = constants.TASK_FG_COLOR
  ui_color = constants.TASK_BG_COLOR

  template_fields = ('conn_id', 'ci360_task_id', )

  def __init__(self, *, conn_id: str, ci360_task_id: str, **kwargs: Any) -> None:
    '''
    Starts a CI 360 task job and defers execution until the task reaches a terminal state.
    The task job metadata is pushed to XCom under the key ci360_task_job.
    
    Parameters

    conn_id
      Airflow connection ID for the CI 360 API connection.

    ci360_task_id
      CI 360 task identifier to execute.
    '''

    super().__init__(**kwargs)
    self.conn_id = conn_id
    self.ci360_task_id = ci360_task_id

  def execute(self, context: Context) -> None:
    config = self._get_config()
    client = CI360Client(config)
    job = client.start_task_job(self.ci360_task_id)
    self.log.info('Started %s', job)
    self.defer(
      trigger=CI360TaskJobTrigger(config.as_dict(), job.as_dict()),
      method_name='execute_complete'
    )

  def execute_complete(self, context: Context, event: Dict[str, Any]) -> None:
    self._finalize_job_execution(
      event_status=event['status'],
      job=CI360TaskJob.from_dict(event['task_job']),
      ti=context['ti'],
      xcom_key=constants.TASK_JOB_XCOM_KEY
    )
