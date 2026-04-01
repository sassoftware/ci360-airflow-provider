#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from typing import Any, Dict

from airflow.triggers.base import TriggerEvent
from airflow.providers.sas_ci360.models import CI360TaskJob
from airflow.providers.sas_ci360.triggers import CI360JobTrigger

class CI360TaskJobTrigger(CI360JobTrigger):
  '''Deferrable trigger that polls CI 360 task job execution status.'''

  def __init__(self, config_dict: Dict[str, Any], job_dict: Dict[str, Any]) -> None:
    super().__init__(
      config_dict=config_dict,
      job=CI360TaskJob.from_dict(job_dict)
    )

  def serialize(self):
    return (
      'airflow.providers.sas_ci360.triggers.task_job_trigger.CI360TaskJobTrigger',
      {
        'config_dict': self.config.as_dict(),
        'job_dict': self.job.as_dict()
      }
    )

  def _get_ci360_job(self) -> CI360TaskJob:
    client = self._get_client()
    return client.get_task_job(self.job.status_href)

  def _trigger_event(self, status: str, job: CI360TaskJob) -> TriggerEvent:
    return TriggerEvent({
      'status': status,
      'task_job': job.as_dict()
    })
