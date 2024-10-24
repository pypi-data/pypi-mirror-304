# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._models import BaseModel

__all__ = ["AccountRead"]


class AccountRead(BaseModel):
    id: int

    name: str

    tenant: str
