from typing import Any, Optional, Iterable
from uuid import UUID

from aiohttp.client import _RequestContextManager
from pydantic import validate_arguments

from .model import Verification, CheckType
from ..resource import Resource
from ..common import PagedResponse


class Verifications(Resource):
    def _proceed(self, verification_id: UUID) -> _RequestContextManager:
        return self._session.post(url=f"{self._api_endpoint}/api/v3/verifications/{verification_id}/proceed")

    @validate_arguments
    async def proceed(self, verification_id: UUID) -> None:
        async with self._proceed(verification_id) as response:
            await self._validate_resp(response, [200], "proceed verification")

    def _create(
        self,
        checks: Iterable[CheckType],
        applicant_id: Optional[UUID] = None,
    ) -> _RequestContextManager:
        body: dict[str, Any] = {"checks_required": checks}
        if applicant_id is not None:
            body["applicant_id"] = str(applicant_id)

        return self._session.post(url=f"{self._api_endpoint}/api/v3/verifications", json=body)

    @validate_arguments
    async def create(
        self,
        checks: Iterable[CheckType],
        applicant_id: Optional[UUID] = None,
    ) -> Verification:
        async with self._create(checks, applicant_id) as response:
            await self._validate_resp(response, [201], "create verification")
            data = await response.json()

        return Verification(**data)

    def _get(self, verification_id: UUID) -> _RequestContextManager:
        return self._session.get(url=f"{self._api_endpoint}/api/v3/verifications/{verification_id}")

    @validate_arguments
    async def get(self, verification_id: UUID) -> Optional[Verification]:
        async with self._get(verification_id) as response:
            await self._validate_resp(response, [200, 404], "find verification")
            if response.status == 404:
                return None
            data = await response.json()
        return Verification(**data)

    def _list(self, page: int = 0, limit: int = 10) -> _RequestContextManager:
        return self._session.get(
            url=f"{self._api_endpoint}/api/v3/verifications", params={"page": page, "limit": limit}
        )

    @validate_arguments
    async def list(self, page: int = 0, limit: int = 10) -> PagedResponse[Verification]:
        async with self._list(page, limit) as response:
            await self._validate_resp(response, [200], "list verifications")
            data = await response.json()
        return PagedResponse[Verification](**data)

    def _list_for_applicant(self, applicant_id: UUID, page: int = 0, limit: int = 10) -> _RequestContextManager:
        return self._session.get(
            url=f"{self._api_endpoint}/api/v3/verifications/applicant/{applicant_id}",
            params={"page": page, "limit": limit},
        )

    @validate_arguments
    async def list_for_applicant(
        self, applicant_id: UUID, page: int = 0, limit: int = 10
    ) -> PagedResponse[Verification]:
        async with self._list_for_applicant(applicant_id, page, limit) as response:
            await self._validate_resp(response, [200], "list verifications for applicant")
            data = await response.json()
        return PagedResponse[Verification](**data)
