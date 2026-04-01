#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from base64 import b64encode
import json
import logging
from typing import Any, Dict
import jwt
import requests

from airflow.providers.sas_ci360 import constants
from airflow.providers.sas_ci360.config import CI360Config
from airflow.providers.sas_ci360.models import CI360SegmentMapJob, CI360TaskJob

log = logging.getLogger(__name__)

class CI360Client:
  def __init__(self, config: CI360Config):
    self.base_url = config.base_url
    self.start_timeout = (config.start_connect_timeout_seconds, config.start_read_timeout_seconds)
    self.status_timeout = (config.status_connect_timeout_seconds, config.status_read_timeout_seconds)
    self.session = requests.Session()
    token = self._authorization_token(config)
    self.session.headers['Authorization'] = f'Bearer {token}'

    if config.https_proxy:
      self.session.proxies['https'] = config.https_proxy

  def start_segment_map_job(self, ci360_segment_map_id: str) -> CI360SegmentMapJob:
    url = self._url('/marketingExecution/segmentMapJobs')
    payload = {
      'segmentMapId': ci360_segment_map_id,
      'version': 1,
      'overrideSchedule': True
    }
    r = self._post(url, payload, timeout=self.start_timeout)
    return CI360SegmentMapJob.from_api_response(r.json())

  def get_segment_map_job(self, segment_map_job_href: str) -> CI360SegmentMapJob:
    r = self._get(segment_map_job_href, timeout=self.status_timeout)
    return CI360SegmentMapJob.from_api_response(r.json())
  
  def start_task_job(self, ci360_task_id: str) -> CI360TaskJob:
    url = self._url('/marketingExecution/taskJobs')
    payload = {
      'taskId': ci360_task_id,
      'version': 1,
      'overrideSchedule': True
    }
    r = self._post(url, payload, timeout=self.start_timeout)
    return CI360TaskJob.from_api_response(r.json())

  def get_task_job(self, task_job_href: str) -> CI360TaskJob:
    r = self._get(task_job_href, timeout=self.status_timeout)
    return CI360TaskJob.from_api_response(r.json())

  def _parse_value(self, value: Any) -> Any:
    if not isinstance(value, str):
      return value
    try:
      return json.loads(value)
    except (ValueError, TypeError):
      return value

  def get_occurrence_properties(self, occurrence_href: str) -> Dict[str, Any]:
    r = self._get(occurrence_href, timeout=self.status_timeout)
    raw = r.json().get('properties')
    if not isinstance(raw, dict):
      return {}
    return { 
      key: self._parse_value(value)
      for key, value in raw.items()
    }

  def test_connection(self) -> tuple[bool, str]:
    url = self._url('/marketingGateway/configuration')
    r = None
    try:
      r = self.session.get(url, timeout=(10.0, 20.0))
      r.raise_for_status()
      try:
        payload = r.json()
      except ValueError:
        return False, f'Invalid JSON response from {r.url} (HTTP {r.status_code}).'

      ap_name = payload.get('agentName', '<unknown>')
      ap_type = payload.get('type', '<unknown>')
      return True, f'Successfully pinged CI 360 access point {ap_name} ({ap_type}): HTTP {r.status_code} on {r.url}.'

    except requests.RequestException as re:
      if r is None:
        return False, f'Connection failed: {re}'
      return False, f'HTTP {r.status_code} on {r.url}: {r.text}'

    except Exception as e:
      return False, f'Unexpected error during connection test: {e}'

  def _authorization_token(self, config: CI360Config) -> str:
    if config.auth_type == constants.CLIENT_SECRET_AUTHENTICATION:
      b64_secret = b64encode(bytes(config.client_secret, encoding='utf8'))
      token = jwt.encode({'clientID': config.tenant_id}, b64_secret, algorithm='HS256')
      return token
    if config.auth_type == constants.JWT_AUTHENTICATION:
      return config.jwt_token
    raise ValueError(f'auth_type must be "{constants.CLIENT_SECRET_AUTHENTICATION}" or "{constants.JWT_AUTHENTICATION}"')
  
  def _url(self, uri: str) -> str:
    if uri.startswith('http://') or uri.startswith('https://'):
      return uri
    return f'{self.base_url}/{uri.lstrip("/")}'

  def _get(self, url: str, **kwargs) -> requests.Response:
    r = None
    try:
      r = self.session.get(url, **kwargs)
      r.raise_for_status()
      return r
    except requests.RequestException:
      if r is not None:
        log.error(
          'GET %s failed: status=%s response=%r',
          r.url,
          r.status_code,
          r.text,
          exc_info=True
        )
      else:
        log.error('GET %s failed.', url, exc_info=True)
      raise

  def _post(self, url: str, payload: Dict[str, Any], **kwargs) -> requests.Response:
    r = None
    try:
      r = self.session.post(url, json=payload, **kwargs)
      r.raise_for_status()
      return r
    except requests.RequestException:
      if r is not None:
        log.error(
          'POST %s failed: payload=%s status=%s response=%r',
          r.url,
          payload,
          r.status_code,
          r.text,
          exc_info=True
        )
      else:
        log.error('POST %s failed: payload=%s', url, payload, exc_info=True)
      raise
