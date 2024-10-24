# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["ProtocolParsingCreateParams"]


class ProtocolParsingCreateParams(TypedDict, total=False):
    file: Required[FileTypes]

    site_ids: Iterable[int]

    title: str
