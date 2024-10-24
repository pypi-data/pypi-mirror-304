# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .user_role_read import UserRoleRead

__all__ = ["UserListResponse"]

UserListResponse: TypeAlias = List[UserRoleRead]
