# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .account_read import AccountRead

__all__ = ["AccountListResponse"]

AccountListResponse: TypeAlias = List[AccountRead]
