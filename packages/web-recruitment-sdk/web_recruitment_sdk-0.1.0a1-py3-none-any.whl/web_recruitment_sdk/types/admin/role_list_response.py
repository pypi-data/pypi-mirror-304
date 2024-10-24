# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .role_read import RoleRead

__all__ = ["RoleListResponse"]

RoleListResponse: TypeAlias = List[RoleRead]
