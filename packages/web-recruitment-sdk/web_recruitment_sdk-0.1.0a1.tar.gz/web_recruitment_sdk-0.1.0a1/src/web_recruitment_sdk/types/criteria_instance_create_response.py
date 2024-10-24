# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .criteria_instance_read import CriteriaInstanceRead

__all__ = ["CriteriaInstanceCreateResponse"]

CriteriaInstanceCreateResponse: TypeAlias = List[CriteriaInstanceRead]
