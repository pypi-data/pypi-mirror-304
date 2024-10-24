# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import date

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..shared.site_read import SiteRead

__all__ = ["PatientMatch", "NextAppointment"]


class NextAppointment(BaseModel):
    date: str


class PatientMatch(BaseModel):
    id: int

    dob: Optional[date] = None

    email: Optional[str] = None

    external_patient_id: str = FieldInfo(alias="externalPatientId")

    family_name: str = FieldInfo(alias="familyName")

    given_name: str = FieldInfo(alias="givenName")

    match_last_updated: Optional[str] = FieldInfo(alias="matchLastUpdated", default=None)

    match_percentage: float = FieldInfo(alias="matchPercentage")

    next_appointment: Optional[NextAppointment] = FieldInfo(alias="nextAppointment", default=None)

    site_id: int = FieldInfo(alias="siteId")

    middle_name: Optional[str] = FieldInfo(alias="middleName", default=None)

    phone: Optional[str] = None

    site: Optional[SiteRead] = None
