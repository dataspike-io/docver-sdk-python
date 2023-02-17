from typing import Generic, TypeVar, Sequence

from pydantic.generics import GenericModel

T = TypeVar("T")


class PagedResponse(GenericModel, Generic[T]):
    data: Sequence[T]
    has_next: bool
