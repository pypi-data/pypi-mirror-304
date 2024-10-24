# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .appointment_read import AppointmentRead

__all__ = ["AppointmentBulkResponse"]

AppointmentBulkResponse: TypeAlias = List[AppointmentRead]
