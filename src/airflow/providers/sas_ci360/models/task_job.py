#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass(frozen=True)
class CI360TaskJob:
  task_id: str
  task_job_id: str
  execution_state: str
  started_timestamp: str
  ended_timestamp: Optional[str]
  status_href: str = field(repr=False)
  occurrence_href: str = field(repr=False)

  @staticmethod
  def from_api_response(payload: Dict[str, Any]) -> CI360TaskJob:
    links = {link['rel']: link for link in payload.get('links', [])}

    self_link = links.get('self')
    if not self_link:
      raise ValueError('Missing self link in task job response')

    occurrence_link = links.get('occurrence')
    if not occurrence_link:
      raise ValueError('Missing occurrence link in task job response')

    return CI360TaskJob(
      task_id=payload['taskId'],
      task_job_id=payload['taskJobId'],
      execution_state=payload['executionState'],
      started_timestamp=payload['startedTimeStamp'],
      ended_timestamp=payload.get('endTimeStamp'),
      status_href=self_link['href'],
      occurrence_href=occurrence_link['href']
    )

  def as_dict(self) -> Dict[str, Any]:
    return {
      'task_id': self.task_id,
      'task_job_id': self.task_job_id,
      'execution_state': self.execution_state,
      'started_timestamp': self.started_timestamp,
      'ended_timestamp': self.ended_timestamp,
      'status_href': self.status_href,
      'occurrence_href': self.occurrence_href
    }

  @staticmethod
  def from_dict(data: Dict[str, Any]) -> CI360TaskJob:
    return CI360TaskJob(
      task_id=data['task_id'],
      task_job_id=data['task_job_id'],
      execution_state=data['execution_state'],
      started_timestamp=data['started_timestamp'],
      ended_timestamp=data.get('ended_timestamp'),
      status_href=data['status_href'],
      occurrence_href=data['occurrence_href']
    )

  @property
  def job_id_label(self) -> str:
    return 'task_job_id'

  @property
  def job_id_value(self) -> str:
    return self.task_job_id
