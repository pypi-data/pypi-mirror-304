# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .site_read import SiteRead

__all__ = ["ProtocolRead", "ProtocolParsing"]


class ProtocolParsing(BaseModel):
    id: int

    file_url: Optional[str] = FieldInfo(alias="fileUrl", default=None)

    job_id: Optional[str] = FieldInfo(alias="jobId", default=None)

    status: Optional[Literal["processing", "error", "success"]] = None

    status_message: Optional[str] = FieldInfo(alias="statusMessage", default=None)


class ProtocolRead(BaseModel):
    id: int

    created_at: datetime = FieldInfo(alias="createdAt")

    external_protocol_id: Optional[str] = FieldInfo(alias="externalProtocolId", default=None)

    protocol_parsing: Optional[ProtocolParsing] = FieldInfo(alias="protocolParsing", default=None)

    title: str

    sites: Optional[List[SiteRead]] = None

    status: Optional[Literal["active", "inactive"]] = None
