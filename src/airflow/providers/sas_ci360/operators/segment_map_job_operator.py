#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict
from airflow.providers.sas_ci360 import constants
from airflow.providers.sas_ci360.client import CI360Client
from airflow.providers.sas_ci360.models import CI360SegmentMapJob
from airflow.providers.sas_ci360.triggers import CI360SegmentMapJobTrigger
from .job_operator import CI360JobOperator

if TYPE_CHECKING:
  from airflow.utils.context import Context

class CI360SegmentMapJobOperator(CI360JobOperator):
  '''Execute a CI 360 segment map, defer until completion'''

  custom_operator_name = constants.SEGMENT_MAP_UI_LABEL
  ui_fgcolor = constants.SEGMENT_MAP_FG_COLOR
  ui_color = constants.SEGMENT_MAP_BG_COLOR

  template_fields = ('conn_id', 'ci360_segment_map_id', )

  def __init__(self, *, conn_id: str, ci360_segment_map_id: str, **kwargs: Any) -> None:
    '''
    Starts a CI 360 segment map job and defers execution until the segment map reaches a terminal state.
    The segment map job metadata is pushed to XCom under the key ci360_segment_map_job.
    
    Parameters

    conn_id
      Airflow connection ID for the CI 360 API connection.

    ci360_segment_map_id
      CI 360 segment map identifier to execute.
    '''

    super().__init__(**kwargs)
    self.conn_id = conn_id
    self.ci360_segment_map_id = ci360_segment_map_id

  def execute(self, context: Context) -> None:
    config = self._get_config()
    client = CI360Client(config)
    job = client.start_segment_map_job(self.ci360_segment_map_id)
    self.log.info('Started %s', job)
    self.defer(
      trigger=CI360SegmentMapJobTrigger(config.as_dict(), job.as_dict()),
      method_name='execute_complete'
    )

  def execute_complete(self, context: Context, event: Dict[str, Any]) -> None:
    self._finalize_job_execution(
      event_status=event['status'],
      job=CI360SegmentMapJob.from_dict(event['segment_map_job']), 
      ti=context['ti'],
      xcom_key=constants.SEGMENT_MAP_JOB_XCOM_KEY
    )
