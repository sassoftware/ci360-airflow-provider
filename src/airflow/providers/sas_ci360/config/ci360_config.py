#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import logging
from typing import Any, Dict
from airflow.providers.sas_ci360 import constants

log = logging.getLogger(__name__)

class CI360Config:
  def __init__(
    self,
    base_url: str,
    auth_type: str,
    tenant_id: str,
    client_secret: str,
    jwt_token: str,
    https_proxy: str,
    poll_interval_seconds: float,
    poll_error_timeout_seconds: float,
    start_connect_timeout_seconds: float,
    start_read_timeout_seconds: float,
    status_connect_timeout_seconds: float,
    status_read_timeout_seconds: float,
  ):
    self.base_url = base_url
    self.auth_type = auth_type
    self.tenant_id = tenant_id
    self.client_secret = client_secret
    self.jwt_token = jwt_token
    self.https_proxy = https_proxy
    self.poll_interval_seconds = poll_interval_seconds
    self.poll_error_timeout_seconds = poll_error_timeout_seconds
    self.start_connect_timeout_seconds = start_connect_timeout_seconds
    self.start_read_timeout_seconds = start_read_timeout_seconds
    self.status_connect_timeout_seconds = status_connect_timeout_seconds
    self.status_read_timeout_seconds = status_read_timeout_seconds

  @classmethod
  def from_connection(
    cls, 
    auth_type: str,
    host: str,
    extra: Dict[str, Any],
    tenant_id: str = '',
    client_secret: str = '',
    jwt_token: str = ''
  ) -> CI360Config:
  
    # check auth_type
    if auth_type == constants.CLIENT_SECRET_AUTHENTICATION:
      if not tenant_id or not client_secret:
        raise ValueError('tenant_id and client_secret required for client-secret authentication')
      if client_secret == constants.MASKED_SECRET:
        raise ValueError(f'Invalid client secret ("{client_secret}"). The value was likely masked by Airflow (Airflow 3 UI test limitation).')
    
    elif auth_type == constants.JWT_AUTHENTICATION:
      if not jwt_token:
        raise ValueError('jwt_token required for jwt authentication')
      if jwt_token == constants.MASKED_SECRET:
        raise ValueError(f'Invalid jwt ("{jwt_token}"). The value was likely masked by Airflow (Airflow 3 UI test limitation).')

    else:
      raise ValueError(f'auth_type must be "{constants.CLIENT_SECRET_AUTHENTICATION}" or "{constants.JWT_AUTHENTICATION}"')

    return cls(
      auth_type = auth_type,
      base_url = cls._base_url(host),
      tenant_id = tenant_id,
      client_secret = client_secret,
      jwt_token = jwt_token,
      https_proxy = extra.get('https_proxy', ''),
      poll_interval_seconds = cls._extra_float(extra, 'poll_interval_seconds', constants.DEFAULT_POLL_INTERVAL_SECONDS, constants.MIN_POLL_INTERVAL_SECONDS),
      poll_error_timeout_seconds = cls._extra_float(extra, 'poll_error_timeout_seconds', constants.DEFAULT_POLL_ERROR_TIMEOUT_SECONDS, constants.MIN_POLL_ERROR_TIMEOUT_SECONDS),
      start_connect_timeout_seconds = cls._extra_float(extra, 'start_connect_timeout_seconds', constants.DEFAULT_START_CONNECT_TIMEOUT_SECONDS),
      start_read_timeout_seconds = cls._extra_float(extra, 'start_read_timeout_seconds', constants.DEFAULT_START_READ_TIMEOUT_SECONDS),
      status_connect_timeout_seconds = cls._extra_float(extra, 'status_connect_timeout_seconds', constants.DEFAULT_STATUS_CONNECT_TIMEOUT_SECONDS),
      status_read_timeout_seconds = cls._extra_float(extra, 'status_read_timeout_seconds', constants.DEFAULT_STATUS_READ_TIMEOUT_SECONDS)
    )

  @staticmethod
  def _extra_float(extra: Dict[str, Any], name: str, default: float, minimum: float = None) -> float:
    raw = extra.get(name, default)
    try:
      value = float(raw)
    except (TypeError, ValueError):
      log.warning('Invalid number %s=%r. Applying default value %s', name, raw, default)
      value = default
    if minimum is None and value <= 0.0:
      log.warning('Expected positive value for %s=%s. Applying default value %s', name, raw, default)
      value = default
    if minimum is not None and value < minimum:
      log.warning('%s=%r below minimum (%s). Capped to %s.', name, raw, minimum, minimum)
      value = minimum
    log.debug('Using %s=%s', name, value)
    return value

  @staticmethod
  def _base_url(host: str) -> str:
    host = host.strip()
    if host.startswith('http://') or host.startswith('https://'):
      return host
    return f'https://{host}'

  @classmethod
  def from_dict(cls, data: Dict[str, Any]) -> CI360Config:
    return cls(
      auth_type = cls._str(data, 'auth_type'),
      base_url = cls._str(data, 'base_url'),
      tenant_id = cls._str(data, 'tenant_id'),
      client_secret = cls._str(data, 'client_secret'),
      jwt_token = cls._str(data, 'jwt_token'),
      https_proxy = cls._str(data, 'https_proxy'),
      poll_interval_seconds = cls._float(data, 'poll_interval_seconds'),
      poll_error_timeout_seconds = cls._float(data, 'poll_error_timeout_seconds'),
      start_connect_timeout_seconds = cls._float(data, 'start_connect_timeout_seconds'),
      start_read_timeout_seconds = cls._float(data, 'start_read_timeout_seconds'),
      status_connect_timeout_seconds = cls._float(data, 'status_connect_timeout_seconds'),
      status_read_timeout_seconds = cls._float(data, 'status_read_timeout_seconds'),
    )

  @staticmethod
  def _str(data: Dict[str, Any], name: str) -> str:
    if name not in data:
      raise ValueError(f'Missing "{name}" in config')
    value = data[name]
    if type(value) != str:
      raise ValueError(f'Invalid "{name}" in config: {value!r}')
    return str(data[name])

  @staticmethod
  def _float(data: Dict[str, Any], name: str) -> float:
    if name not in data:
      raise ValueError(f'Missing "{name}" in config')
    raw = data[name]
    try:
      value = float(raw)
    except (TypeError, ValueError):
      raise ValueError(f'Invalid "{name}" in config: {raw!r}')
    return value

  def as_dict(self) -> Dict[str, Any]:
    return {
      'auth_type': self.auth_type,
      'base_url': self.base_url,
      'tenant_id': self.tenant_id,
      'client_secret': self.client_secret,
      'jwt_token': self.jwt_token,
      'https_proxy': self.https_proxy,
      'poll_interval_seconds': self.poll_interval_seconds,
      'poll_error_timeout_seconds': self.poll_error_timeout_seconds,
      'start_connect_timeout_seconds': self.start_connect_timeout_seconds,
      'start_read_timeout_seconds': self.start_read_timeout_seconds,
      'status_connect_timeout_seconds': self.status_connect_timeout_seconds,
      'status_read_timeout_seconds': self.status_read_timeout_seconds,
    }
