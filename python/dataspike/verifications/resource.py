from typing import Any, Sequence, Optional
from uuid import UUID

from aiohttp import ClientResponse
from pydantic import validate_arguments

from model import Verification
from ..documents.model import DocumentType
from ..resource import Resource


class Verifications(Resource):
    async def _proceed(self, verification_id: UUID) -> ClientResponse:
        return await self._session.post(url=f"{self._api_endpoint}/api/v3/verifications/{verification_id}/proceed")

    @validate_arguments
    async def proceed(self, verification_id: UUID) -> None:
        response = await self._proceed(verification_id)
        await self._validate_resp(response, [200], "proceed verification")

    async def _create(
        self,
        checks_required: Sequence[DocumentType],
        applicant_id: Optional[UUID] = None,
    ) -> ClientResponse:
        body: dict[str, Any] = {"checks_required": checks_required}
        if applicant_id is not None:
            body["applicant_id"] = str(applicant_id)

        return await self._session.post(url=f"{self._api_endpoint}/api/v3/verifications", json=body)

    @validate_arguments
    async def create(
        self,
        checks_required: Sequence[DocumentType],
        applicant_id: Optional[UUID] = None,
    ) -> Verification:
        response = await self._create(checks_required, applicant_id)
        await self._validate_resp(response, [201], "create verification")
        data = await response.json()
        self._uuid_ids(data, "id", "applicant_id")

        return Verification(**data)

    async def _get(self, verification_id: UUID) -> ClientResponse:
        return await self._session.get(url=f"{self._api_endpoint}/api/v3/verifications/{verification_id}")

    @validate_arguments
    async def get(self, verification_id: UUID) -> Verification:
        response = await self._get(verification_id)

        await self._validate_resp(response, [200], "get verification")
        data = await response.json()
        self._uuid_ids(data, "id", "applicant_id")
        return Verification(**data)

    @validate_arguments
    async def find(self, verification_id: UUID) -> Optional[Verification]:
        response = await self._get(verification_id)

        await self._validate_resp(response, [200, 404], "find verification")
        if response.status == 404:
            return None
        data = await response.json()
        self._uuid_ids(data, "id", "applicant_id")
        return Verification(**data)
