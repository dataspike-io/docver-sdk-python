import dataclasses

from typing import Optional

from aiohttp import ClientResponse
from pydantic import validate_arguments
from ..resource import Resource
from ..common import PagedResponse
from .model import Applicant, ApplicantInfo
from uuid import UUID


class Applicants(Resource):
    async def _get(self, applicant_id: UUID) -> ClientResponse:
        return await self._session.get(url=f"{self._api_endpoint}/api/v3/applicants/{applicant_id}")

    @validate_arguments
    async def get(self, applicant_id: UUID) -> Applicant:
        response = await self._get(applicant_id)
        await self._validate_resp(response, [200], "get applicant")
        data = await response.json()
        return Applicant(**data)

    @validate_arguments
    async def find(self, applicant_id: UUID) -> Optional[Applicant]:
        response = await self._get(applicant_id)
        if response.status == 404:
            return None
        await self._validate_resp(response, [200], "get applicant")
        data = await response.json()
        return Applicant(**data)

    async def _create(self, external_id: Optional[str] = None, info: Optional[ApplicantInfo] = None) -> ClientResponse:
        body = {}
        if external_id is not None:
            body["external_id"] = external_id
        if info is not None:
            body["info"] = dataclasses.asdict(info)
        return await self._session.post(url=f"{self._api_endpoint}/api/v3/applicants", json=body)

    @validate_arguments
    async def create(self, external_id: Optional[str] = None, info: Optional[ApplicantInfo] = None) -> UUID:
        response = await self._create(external_id, info)

        await self._validate_resp(response, [201], "create applicant")

        data = await response.json()
        return UUID(data["id"])

    async def _list(self, page: int = 0, limit: int = 10) -> ClientResponse:
        return await self._session.get(url=f"{self._api_endpoint}/api/v3/applicants?page={page}&?limit={limit}")

    @validate_arguments
    async def list(self, page: int = 0, limit: int = 10) -> PagedResponse[Applicant]:
        response = await self._list(page, limit)
        await self._validate_resp(response, [200], "list applicants")
        data = await response.json()
        return PagedResponse[Applicant](**data)

    async def _delete(self, applicant_id: UUID) -> ClientResponse:
        return await self._session.delete(url=f"{self._api_endpoint}/api/v3/applicants/{applicant_id}")

    @validate_arguments
    async def delete(self, applicant_id: UUID) -> None:
        response = await self._delete(applicant_id)
        await self._validate_resp(response, [200], "delete applicant")
