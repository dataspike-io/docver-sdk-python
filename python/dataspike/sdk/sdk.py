from uuid import UUID

from aiohttp.client import _RequestContextManager
from pydantic import validate_arguments

from ..resource import Resource


class Sdk(Resource):
    def _create_token(self, applicant_id) -> _RequestContextManager:
        return self._session.post(
            url=f"{self._api_endpoint}/api/v3/sdk_token", json={"applicant_id": str(applicant_id)}
        )

    @validate_arguments
    async def create_token(self, applicant_id: UUID) -> str:
        async with self._create_token(applicant_id) as response:
            await self._validate_resp(response, [200, 201], "sdk token create")
            data = await response.json()
        return data["token"]
