# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .account_read import AccountRead

__all__ = ["UserWithAccount"]


class UserWithAccount(BaseModel):
    id: int

    account_id: int = FieldInfo(alias="accountId")

    email: str

    role_id: int = FieldInfo(alias="roleId")

    account: Optional[AccountRead] = None
