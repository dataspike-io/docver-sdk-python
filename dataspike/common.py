from __future__ import annotations

from typing import Generic, TypeVar, List
from pydantic import BaseModel

__all__ = ["PagedResponse"]

T = TypeVar("T")


class PagedResponse(BaseModel, Generic[T]):
    data: List[T]
    has_next: bool
