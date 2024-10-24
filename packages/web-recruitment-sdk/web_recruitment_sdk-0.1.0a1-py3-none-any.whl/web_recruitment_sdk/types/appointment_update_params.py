# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["AppointmentUpdateParams"]


class AppointmentUpdateParams(TypedDict, total=False):
    date: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    patient_id: Required[Annotated[int, PropertyInfo(alias="patientId")]]
