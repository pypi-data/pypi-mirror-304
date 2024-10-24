# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import date
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PatientCreateParams"]


class PatientCreateParams(TypedDict, total=False):
    dob: Required[Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]]

    email: Required[Optional[str]]

    external_patient_id: Required[Annotated[str, PropertyInfo(alias="externalPatientId")]]

    family_name: Required[Annotated[str, PropertyInfo(alias="familyName")]]

    given_name: Required[Annotated[str, PropertyInfo(alias="givenName")]]

    site_id: Required[Annotated[int, PropertyInfo(alias="siteId")]]

    middle_name: Annotated[Optional[str], PropertyInfo(alias="middleName")]

    phone: Optional[str]
