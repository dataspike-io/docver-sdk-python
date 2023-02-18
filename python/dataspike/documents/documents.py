from typing import Optional
from uuid import UUID

from aiohttp import FormData
from pydantic import validate_arguments

from .model import DocumentSide, DocumentType
from ..resource import Resource


class Documents(Resource):
    @validate_arguments
    async def upload(
        self,
        applicant_id: UUID,
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> UUID:
        data = FormData()
        data.add_field("file", file, content_type="image/*")
        data.add_field("document_type", document_type)
        if document_side:
            data.add_field("side", document_side)
        async with self._session.post(url=f"{self._api_endpoint}/api/v3/upload/{applicant_id}", data=data) as response:
            await self._validate_resp(response, [200, 201], "upload document")
            data = await response.json()
            return data["document_id"]
