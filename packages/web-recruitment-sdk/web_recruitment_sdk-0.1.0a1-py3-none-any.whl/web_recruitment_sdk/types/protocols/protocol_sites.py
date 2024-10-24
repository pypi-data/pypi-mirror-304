# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ProtocolSites"]


class ProtocolSites(BaseModel):
    protocol_id: int = FieldInfo(alias="protocolId")

    site_id: int = FieldInfo(alias="siteId")

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)

    updated_at: Optional[datetime] = FieldInfo(alias="updatedAt", default=None)
