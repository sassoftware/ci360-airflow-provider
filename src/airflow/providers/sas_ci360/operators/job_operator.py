#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

import json
from typing import Any, Dict
from airflow.exceptions import AirflowException
from airflow.models.taskinstance import TaskInstance

from airflow.providers.sas_ci360 import constants
from airflow.providers.sas_ci360.compat import BaseOperator
from airflow.providers.sas_ci360.config import CI360Config
from airflow.providers.sas_ci360.hooks import CI360Hook
from airflow.providers.sas_ci360.client import CI360Client
from airflow.providers.sas_ci360.typing import CI360JobLike

class CI360JobOperator(BaseOperator):
  '''
  Internal base class for CI 360 job operators.
  Provides shared configuration and occurrence-handling utilities.
  '''

  def _get_config(self) -> CI360Config:
    if not hasattr(self, '_ci360_config'):
      hook = CI360Hook.from_connection_id(self.conn_id)
      self._ci360_config = hook.get_config()
    return self._ci360_config

  def _get_occurrence_properties(self, occurrence_href: str) -> Dict[str, Any]:
    client = CI360Client(self._get_config())
    try:
      return client.get_occurrence_properties(occurrence_href)
    except Exception:
      self.log.warning('Failed fetching occurrence from %s', occurrence_href)
      return {}

  def _finalize_job_execution(
    self,
    event_status: str,
    job: CI360JobLike, 
    ti: TaskInstance,
    xcom_key: str
  ) -> None:

    # Always attempt to fetch occurrence properties. Failed executions may expose valuable diagnostics.
    occurrence_properties = self._get_occurrence_properties(job.occurrence_href)

    # Push XCom message 
    xcom_value = job.as_dict()
    xcom_value['occurrence_properties'] = occurrence_properties
    ti.xcom_push(key=xcom_key, value=xcom_value)
 
    # Handle status
    properties_str = json.dumps(occurrence_properties, separators=(',', ':'))
    if event_status == constants.EVENT_STATUS_SUCCESS:
      self.log.info('Succeeded %s', job)
      self.log.info('%s', properties_str)
    elif event_status == constants.EVENT_STATUS_FAILED:
      self.log.error('Failed %s', job)
      self.log.error('%s', properties_str)
      raise AirflowException('CI 360 job failed.')
    elif event_status == constants.EVENT_STATUS_ERROR:
      self.log.error('Error processing %s', job)
      raise AirflowException('Error processing CI 360 job.')
    else:
      raise AirflowException(f'Unexpected status: "{event_status}"')
