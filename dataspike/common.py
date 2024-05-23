from __future__ import annotations

from typing import Generic, TypeVar, List

from pydantic.generics import GenericModel

__all__ = ["PagedResponse"]

T = TypeVar("T")


class PagedResponse(GenericModel, Generic[T]):
    data: List[T]
    has_next: bool
