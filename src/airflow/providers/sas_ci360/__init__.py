#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from importlib.metadata import version, PackageNotFoundError

from airflow.providers.sas_ci360 import constants

try:
  __version__ = version('sas-ci360-airflow-provider')
except PackageNotFoundError:
  __version__ = '0.0.0'

def get_provider_info():
  return {
    'package-name': 'sas-ci360-airflow-provider',
    'name': 'CI360 Airflow Provider',
    'description': 'Apache Airflow provider for SAS Customer Intelligence 360',
    'versions': [__version__],
    'hook-class-names': [
      'airflow.providers.sas_ci360.hooks.CI360ClientSecretHook',
      'airflow.providers.sas_ci360.hooks.CI360JwtHook'
    ],
    'operator-class-names': [
      'airflow.providers.sas_ci360.operators.CI360TaskJobOperator',
      'airflow.providers.sas_ci360.operators.CI360SegmentMapJobOperator'
    ],
    'trigger-class-names': [
      'airflow.providers.sas_ci360.triggers.CI360TaskJobTrigger',
      'airflow.providers.sas_ci360.triggers.CI360SegmentMapJobTrigger'
    ],
    'connection-types': [
        {
          'connection-type': constants.CLIENT_SECRET_CONNECTION,
          'hook-class-name': 'airflow.providers.sas_ci360.hooks.CI360ClientSecretHook'
        },
        {
          'connection-type': constants.JWT_CONNECTION,
          'hook-class-name': 'airflow.providers.sas_ci360.hooks.CI360JwtHook'
        }

    ],
    'source': 'https://github.com/sassoftware/ci360-airflow-provider',
    'project-url': 'https://github.com/sassoftware/ci360-airflow-provider',
    'documentation': 'https://github.com/sassoftware/ci360-airflow-provider'
  }
