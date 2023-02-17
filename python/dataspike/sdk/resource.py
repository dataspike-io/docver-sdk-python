from uuid import UUID

from aiohttp import ClientResponse
from pydantic import validate_arguments

from ..resource import Resource


class Sdk(Resource):
    async def _create_token(self, applicant_id) -> ClientResponse:
        return await self._session.post(
            url=f"{self._api_endpoint}/api/v3/sdk_token", json={"applicant_id": str(applicant_id)}
        )

    @validate_arguments
    async def create_token(self, applicant_id: UUID) -> str:
        response = await self._create_token(applicant_id)
        await self._validate_resp(response, [200, 201], "sdk token create")
        data = await response.json()
        return data["token"]
