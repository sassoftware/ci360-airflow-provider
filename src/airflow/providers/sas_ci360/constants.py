#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0


# ---------------------------------------------------------------------------
# Airflow operator appearance (displayed in UI)
# ---------------------------------------------------------------------------

TASK_UI_LABEL = 'SAS® CI 360 Task'
TASK_FG_COLOR = '#000000'
TASK_BG_COLOR = '#c4defd' # Light Blue

SEGMENT_MAP_UI_LABEL = 'SAS® CI 360 Segment Map'
SEGMENT_MAP_FG_COLOR = '#000000'
SEGMENT_MAP_BG_COLOR = '#dee8e3' # Muted Green


# ---------------------------------------------------------------------------
# Airflow connection types (UI / metadata identifiers)
# ---------------------------------------------------------------------------

CLIENT_SECRET_CONNECTION = 'sas-ci360-client-secret'
JWT_CONNECTION = 'sas-ci360-jwt'


# ---------------------------------------------------------------------------
# Airflow hook names (displayed in UI)
# ---------------------------------------------------------------------------

CLIENT_SECRET_HOOK_NAME = 'SAS® Customer Intelligence 360 - client secret'
JWT_HOOK_NAME = 'SAS® Customer Intelligence 360 - jwt'


# ---------------------------------------------------------------------------
# Authentication modes (runtime behavior)
# ---------------------------------------------------------------------------

CLIENT_SECRET_AUTHENTICATION = 'client-secret'
JWT_AUTHENTICATION = 'jwt'


# ---------------------------------------------------------------------------
# Security / masking
# ---------------------------------------------------------------------------

MASKED_SECRET = '***'


# ---------------------------------------------------------------------------
# Trigger → operator event statuses
# ---------------------------------------------------------------------------

EVENT_STATUS_SUCCESS = 'success'
EVENT_STATUS_FAILED = 'failed'
EVENT_STATUS_ERROR = 'error'


# ---------------------------------------------------------------------------
# CI 360 job execution states (as returned by CI 360 APIs)
# ---------------------------------------------------------------------------

TERMINAL_SUCCESS_STATES = {'success'}
TERMINAL_FAILURE_STATES = {'failure'}


# ---------------------------------------------------------------------------
# REST client timeouts (seconds)
# ---------------------------------------------------------------------------

DEFAULT_START_CONNECT_TIMEOUT_SECONDS = 20.0
DEFAULT_START_READ_TIMEOUT_SECONDS = 120.0
DEFAULT_STATUS_CONNECT_TIMEOUT_SECONDS = 5.0
DEFAULT_STATUS_READ_TIMEOUT_SECONDS = 30.0

DEFAULT_POLL_INTERVAL_SECONDS = 20.0
DEFAULT_POLL_ERROR_TIMEOUT_SECONDS = 1800.0

MIN_POLL_INTERVAL_SECONDS = 5.0
MIN_POLL_ERROR_TIMEOUT_SECONDS = 60.0


# ---------------------------------------------------------------------------
# XCom keys
# ---------------------------------------------------------------------------

TASK_JOB_XCOM_KEY = 'ci360_task_job'
SEGMENT_MAP_JOB_XCOM_KEY = 'ci360_segment_map_job'
