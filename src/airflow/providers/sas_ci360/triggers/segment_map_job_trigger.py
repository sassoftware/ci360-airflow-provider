#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from typing import Any, Dict

from airflow.triggers.base import TriggerEvent
from airflow.providers.sas_ci360.models import CI360SegmentMapJob
from airflow.providers.sas_ci360.triggers import CI360JobTrigger

class CI360SegmentMapJobTrigger(CI360JobTrigger):
  '''Deferrable trigger that polls CI 360 segment map job execution status.'''

  def __init__(self, config_dict: Dict[str, Any], job_dict: Dict[str, Any]) -> None:
    super().__init__(
      config_dict=config_dict,
      job=CI360SegmentMapJob.from_dict(job_dict)
    )

  def serialize(self):
    return (
      'airflow.providers.sas_ci360.triggers.segment_map_job_trigger.CI360SegmentMapJobTrigger',
      {
        'config_dict': self.config.as_dict(),
        'job_dict': self.job.as_dict()
      }
    )

  def _get_ci360_job(self) -> CI360SegmentMapJob:
    client = self._get_client()
    return client.get_segment_map_job(self.job.status_href)

  def _trigger_event(self, status: str, job: CI360SegmentMapJob) -> TriggerEvent:
    return TriggerEvent({
      'status': status,
      'segment_map_job': job.as_dict()
    })
