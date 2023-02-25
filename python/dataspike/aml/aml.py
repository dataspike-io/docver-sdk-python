from uuid import UUID

from aiohttp.client import _RequestContextManager
from pydantic import validate_arguments

from .model import AMLSearchRequest, AMLResponse, AMLEntity
from ..resource import Resource

__all__ = ["AML"]


class AML(Resource):
    def _search(self, request: AMLSearchRequest) -> _RequestContextManager:
        return self._session.post(url=f"{self._api_endpoint}/api/v3/aml/search", json=request)

    def _get(self, id: UUID) -> _RequestContextManager:
        return self._session.get(url=f"{self._api_endpoint}/api/v3/aml/search/{id}")

    @validate_arguments
    async def search(self, request: AMLSearchRequest) -> AMLResponse:
        async with self._search(request) as response:
            await self._validate_resp(response, [200], "aml search")
            data = await response.json()
            return AMLResponse(**data)

    @validate_arguments
    async def get(self, id: UUID) -> AMLEntity:
        async with self._get(id) as response:
            await self._validate_resp(response, [200], "aml get")
            data = await response.json()
            return AMLEntity(**data)
