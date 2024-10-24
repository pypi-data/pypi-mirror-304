# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CriteriaInstanceRead"]


class CriteriaInstanceRead(BaseModel):
    id: int

    answer: Literal["yes", "no", "unsure"]

    criteria_id: int = FieldInfo(alias="criteriaId")

    patient_id: int = FieldInfo(alias="patientId")

    explanation: Optional[str] = None
