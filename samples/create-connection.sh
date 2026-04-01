#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

airflow connections add 'ci360_bct05' \
  --conn-type 'sas-ci360-client-secret' \
  --conn-description 'GCIE Training 05 Sandbox - General Agent' \
  --conn-host 'extapigwservice-training.ci360.sas.com' \
  --conn-login '***' \
  --conn-password '***'
