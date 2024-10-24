# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ProtocolUpdateParams"]


class ProtocolUpdateParams(TypedDict, total=False):
    external_protocol_id: Annotated[Optional[str], PropertyInfo(alias="externalProtocolId")]

    status: Optional[Literal["active", "inactive"]]

    title: Optional[str]
