import dataclasses
from typing import Optional
from uuid import UUID

from aiohttp.client import _RequestContextManager
from pydantic import validate_arguments

from .model import Applicant, ApplicantInfo
from ..common import PagedResponse
from ..resource import Resource


class Applicants(Resource):
    def _get(self, applicant_id: UUID) -> _RequestContextManager:
        return self._session.get(url=f"{self._api_endpoint}/api/v3/applicants/{applicant_id}")

    def _get_by_external_id(self, external_id: str) -> _RequestContextManager:
        return self._session.get(url=f"{self._api_endpoint}/api/v3/applicants/by_external_id/{external_id}")

    @validate_arguments
    async def get(self, applicant_id: UUID) -> Optional[Applicant]:
        async with self._get(applicant_id) as response:
            if response.status == 404:
                return None
            await self._validate_resp(response, [200], "get applicant")
            data = await response.json()
        return Applicant(**data)

    @validate_arguments
    async def get_by_external_id(self, external_id: str) -> Optional[Applicant]:
        async with self._get_by_external_id(external_id) as response:
            if response.status == 404:
                return None
            await self._validate_resp(response, [200], "get applicant")
            data = await response.json()
        return Applicant(**data)

    def _create(
        self, external_id: Optional[str] = None, info: Optional[ApplicantInfo] = None
    ) -> _RequestContextManager:
        body = {}
        if external_id is not None:
            body["external_id"] = external_id
        if info is not None:
            body["info"] = dataclasses.asdict(info)
        return self._session.post(url=f"{self._api_endpoint}/api/v3/applicants", json=body)

    @validate_arguments
    async def create(self, external_id: Optional[str] = None, info: Optional[ApplicantInfo] = None) -> UUID:
        async with self._create(external_id, info) as response:
            await self._validate_resp(response, [201], "create applicant")
            data = await response.json()
        return UUID(data["id"])

    def _list(self, page: int = 0, limit: int = 10) -> _RequestContextManager:
        return self._session.get(url=f"{self._api_endpoint}/api/v3/applicants", params={"page": page, "limit": limit})

    @validate_arguments
    async def list(self, page: int = 0, limit: int = 10) -> PagedResponse[Applicant]:
        async with self._list(page, limit) as response:
            await self._validate_resp(response, [200], "list applicants")
            data = await response.json()
        return PagedResponse[Applicant](**data)

    def _delete(self, applicant_id: UUID) -> _RequestContextManager:
        return self._session.delete(url=f"{self._api_endpoint}/api/v3/applicants/{applicant_id}")

    @validate_arguments
    async def delete(self, applicant_id: UUID) -> None:
        async with self._delete(applicant_id) as response:
            await self._validate_resp(response, [200], "delete applicant")
