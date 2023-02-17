from typing import Generic, TypeVar, Sequence
from pydantic.generics import GenericModel

__all__ = ["PagedResponse"]

T = TypeVar("T")


class PagedResponse(GenericModel, Generic[T]):
    data: Sequence[T]
    has_next: bool
