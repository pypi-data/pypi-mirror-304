# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AccountCreateParams"]


class AccountCreateParams(TypedDict, total=False):
    name: Required[str]

    tenant: Required[str]

    tenant_lookup_identifier: Required[Annotated[str, PropertyInfo(alias="tenantLookupIdentifier")]]
