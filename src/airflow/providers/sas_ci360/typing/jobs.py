#Copyright © 2026, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#SPDX-License-Identifier: Apache-2.0

from typing import Any, Dict, Protocol

class CI360JobLike(Protocol):
  occurrence_href: str
  status_href: str
  execution_state: str | None

  def as_dict(self) -> Dict[str, Any]:
    ...

  @property
  def job_id_label(self) -> str:
    ...

  @property
  def job_id_value(self) -> str:
    ...
