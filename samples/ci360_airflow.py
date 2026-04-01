#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0


from datetime import datetime
from airflow import DAG
from airflow.providers.sas_ci360.operators import CI360TaskJobOperator, CI360SegmentMapJobOperator

with DAG(
  dag_id='ci360_sample_dag_2',
  start_date=datetime(2025, 1, 1),
  schedule=None,
  catchup=False,
) as dag:

  segment_map = CI360SegmentMapJobOperator(
    conn_id='ci360_bct05',
    task_id='MAP_487',
    ci360_segment_map_id='4d95d113-ac89-4d60-9a6c-6c2a60b0e1b3',
  )

  dm_task = CI360TaskJobOperator(
    conn_id='ci360_bct05',
    task_id='TSK_1370',
    ci360_task_id='bc019976-fc25-434f-bf47-1bfd6bead98e',
  )

  segment_map >> dm_task  

