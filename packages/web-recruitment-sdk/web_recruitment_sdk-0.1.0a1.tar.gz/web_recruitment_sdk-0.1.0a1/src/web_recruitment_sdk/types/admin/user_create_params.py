# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["UserCreateParams"]


class UserCreateParams(TypedDict, total=False):
    account_id: Required[Annotated[int, PropertyInfo(alias="accountId")]]

    email: Required[str]

    role_id: Required[Annotated[int, PropertyInfo(alias="roleId")]]
