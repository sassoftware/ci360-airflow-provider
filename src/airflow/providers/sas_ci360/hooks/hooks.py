#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from abc import ABC, abstractmethod
import json
from typing import Any, Dict
from airflow.exceptions import AirflowException
from airflow.providers.sas_ci360 import constants, compat
from airflow.providers.sas_ci360.client import CI360Client
from airflow.providers.sas_ci360.config import CI360Config

class CI360Hook(compat.BaseHook, ABC):
  conn_name_attr = 'conn_id'

  def __init__(self, conn_id):
    super().__init__()
    self.conn_id = conn_id
    self.connection = compat.get_connection(conn_id)
    self.extra = self._load_extra()

  @abstractmethod
  def get_config(self) -> CI360Config:
    ...

  @classmethod
  def from_connection_id(cls, conn_id: str) -> CI360Hook:
    conn_type = compat.get_connection(conn_id).conn_type
    if conn_type == constants.CLIENT_SECRET_CONNECTION:
      return CI360ClientSecretHook(conn_id)
    if conn_type == constants.JWT_CONNECTION:
      return CI360JwtHook(conn_id)
    raise AirflowException(f'Unsupported connection type "{conn_type}" for CI 360 connection "{conn_id}"')

  def _load_extra(self) -> Dict[str, Any]:
    if not self.connection.extra:
      return {}
    try:
      return json.loads(self.connection.extra)
    except Exception as e:
      raise AirflowException(f'Invalid extra JSON in CI 360 connection "{self.conn_id}"') from e

  def test_connection(self) -> tuple[bool, str]:
    try:
      config = self.get_config()
    except Exception as e:
      self.log.exception('Failed to build CI360 configuration')
      return False, f'Config error: {e}'
    try:
      client = CI360Client(config)
    except Exception as e:
      self.log.exception('Failed to create CI360 client')
      return False, f'Client error: {e}'
    success, message = client.test_connection()
    self.log.info('Success=%s: %s', success, message)
    return success, message

class CI360ClientSecretHook(CI360Hook):
  conn_type = constants.CLIENT_SECRET_CONNECTION
  hook_name = constants.CLIENT_SECRET_HOOK_NAME

  @staticmethod
  def get_ui_field_behaviour() -> Dict[str, Any]:
    return {
      'relabeling': {
        'host': 'External gateway host',
        'login': 'Tenant ID',
        'password': 'Client secret'
      },
      'hidden_fields': ['port', 'schema'],
      'placeholders': {
        'host': 'extapigwservice-<env>.ci360.sas.com',
        'login': 'tenant-id',
        'password': 'client-secret'
      }
    }

  def get_config(self) -> CI360Config:
    self.log.info('Loaded CI360 connection (%s)', self.connection.get_uri())

    if not self.connection.host:
      raise AirflowException('CI 360 connection requires gateway host')
    if not self.connection.login:
      raise AirflowException('CI 360 connection requires tenant id (login)')
    if not self.connection.password:
      raise AirflowException('CI 360 connection requires client secret')

    return CI360Config.from_connection(
      auth_type = constants.CLIENT_SECRET_AUTHENTICATION,
      host = self.connection.host,
      tenant_id = self.connection.login,
      client_secret = self.connection.password,
      extra = self.extra
    )

class CI360JwtHook(CI360Hook):
  conn_type = constants.JWT_CONNECTION
  hook_name = constants.JWT_HOOK_NAME

  @staticmethod
  def get_ui_field_behaviour():
    return {
      'relabeling': {
        'host': 'External gateway host',
        'password': 'Access token (jwt)'
      },
      'hidden_fields': ['port', 'schema', 'login'],
      'placeholders': {
        'host': 'extapigwservice-<env>.ci360.sas.com',
        'password': 'access-token'
      }
    }

  def get_config(self) -> CI360Config:
    self.log.info('Loaded CI360 connection (%s)', self.connection.get_uri())

    if not self.connection.host:
      raise AirflowException('CI 360 connection requires Gateway host')
    if not self.connection.password:
      raise AirflowException('CI 360 connection requires Access Token')

    return CI360Config.from_connection(
      auth_type = constants.JWT_AUTHENTICATION,
      host = self.connection.host,
      jwt_token = self.connection.password,
      extra = self.extra
    )
