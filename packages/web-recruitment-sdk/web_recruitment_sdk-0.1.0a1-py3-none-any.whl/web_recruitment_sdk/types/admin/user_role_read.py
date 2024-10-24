# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["UserRoleRead"]


class UserRoleRead(BaseModel):
    id: int

    account_id: int = FieldInfo(alias="accountId")

    email: str

    role: str
