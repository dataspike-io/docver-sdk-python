from typing import Generic, TypeVar

from pydantic.generics import GenericModel

__all__ = ["PagedResponse"]

T = TypeVar("T")


class PagedResponse(GenericModel, Generic[T]):
    data: list[T]
    has_next: bool
