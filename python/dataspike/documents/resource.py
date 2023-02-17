from typing import Optional

from aiohttp import ClientResponse
from pydantic import validate_arguments
from uuid import UUID
from model import DocumentSide, DocumentType
from ..resource import Resource


class Documents(Resource):
    async def _upload(
        self,
        applicant_id: UUID,
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> ClientResponse:
        return await self._session.post(
            url=f"{self._api_endpoint}/api/v3/upload/{applicant_id}",
            headers={"Content-Type": None},
            files={"file": ("file", file, "image/*")},
            data={"document_type": document_type, "side": document_side},
        )

    @validate_arguments
    async def upload(
        self,
        applicant_id: UUID,
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> UUID:
        response = await self._upload(applicant_id, document_type, file, document_side)
        await self._validate_resp(response, [200, 201], "upload document")
        data = await response.json()
        return UUID(data["document_id"])
