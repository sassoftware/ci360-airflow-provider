#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod
import asyncio
import time
from typing import Any, Dict

from airflow.triggers.base import BaseTrigger
from airflow.providers.sas_ci360 import constants
from airflow.providers.sas_ci360.client import CI360Client
from airflow.providers.sas_ci360.config import CI360Config
from airflow.providers.sas_ci360.typing import CI360JobLike

class CI360JobTrigger(BaseTrigger, ABC):
  '''
  Internal base class for CI 360 job Triggers.
  Shared polling, error handling, and lifecycle logic for concrete CI 360 job triggers.
  '''

  def __init__(self, config_dict: Dict[str, Any], job: CI360JobLike) -> None:
    super().__init__()
    self.config = CI360Config.from_dict(config_dict)
    self.job = job
    self.client: CI360Client | None = None

  def _get_client(self) -> CI360Client:
    if self.client is None:
      self.client = CI360Client(self.config)
    return self.client

  @abstractmethod
  def _get_ci360_job(self) -> CI360JobLike:
    ...

  @abstractmethod
  def _trigger_event(self, status: str, job: CI360JobLike):
    ...

  async def run(self):
    poll_interval_seconds = self.config.poll_interval_seconds
    poll_error_timeout_seconds = self.config.poll_error_timeout_seconds
    job = self.job

    first_poll_error_at = None
    self.log.info('Looping for job status (%s=%s)', job.job_id_label, job.job_id_value)
    try:
      while True:
        try:
          job = await asyncio.to_thread(self._get_ci360_job)
          first_poll_error_at = None
          self.log.info('%s', job)
        except Exception as exc:
          now = time.monotonic()
          first_poll_error_at = first_poll_error_at or now
          poll_error_seconds = now - first_poll_error_at
          self.log.warning('Error fetching CI 360 job (%.1fs elapsed): %s', poll_error_seconds, exc, exc_info=True)
          self.client = None
          if poll_error_seconds > poll_error_timeout_seconds:
            msg = f'CI 360 status polling exceeded timeout of {poll_error_timeout_seconds} seconds'
            self.log.error(msg)
            yield self._trigger_event(constants.EVENT_STATUS_ERROR, job)
            return
          await asyncio.sleep(poll_interval_seconds)
          continue

        state = (job.execution_state or '').strip().lower()

        if state in constants.TERMINAL_SUCCESS_STATES:
          yield self._trigger_event(constants.EVENT_STATUS_SUCCESS, job)
          return

        if state in constants.TERMINAL_FAILURE_STATES:
          yield self._trigger_event(constants.EVENT_STATUS_FAILED, job)
          return

        await asyncio.sleep(poll_interval_seconds)

    except asyncio.CancelledError:
      self.log.error('CI 360 trigger cancelled for %s', job)
      yield self._trigger_event(constants.EVENT_STATUS_ERROR, job)
      return
    except Exception as exc:
      self.log.exception('CI 360 trigger crashed for %s', job)
      yield self._trigger_event(constants.EVENT_STATUS_ERROR, job)
      return
