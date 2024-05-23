from typing import Optional, Union
from uuid import UUID
import filetype

from aiohttp import FormData, ClientResponse
from pydantic import validate_arguments

from .model import DocumentSide, DocumentType, Document
from ..resource import Resource


class Documents(Resource):
    async def _upload(
        self,
        upload_to: Union[UUID, str],
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> UUID:
        """
        Uploads document for applicant.
        Use DocumentType with side DocumentType.IdCardFront for example
        or pass document_side parameter.
        """
        data = FormData()
        content_type = None
        try:
            content_type = filetype.guess(file)
            if content_type:
                content_type = content_type.mime
        except TypeError:
            pass

        data.add_field("file", file, content_type=content_type)
        data.add_field("document_type", document_type)
        if document_side:
            data.add_field("side", document_side)
        async with self._session.post(url=f"{self._api_endpoint}/api/v3/upload/{upload_to}", data=data) as response:
            await self._validate_resp(response, [200, 201], "upload document")
            data = await response.json()
            return UUID(data["document_id"])

    @validate_arguments
    async def upload(
        self,
        applicant_id: UUID,
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> UUID:
        """
        Uploads document for applicant.
        Use DocumentType with side DocumentType.IdCardFront for example
        or pass document_side parameter.
        """
        return await self._upload(applicant_id, document_type, file, document_side)

    @validate_arguments
    async def _sdk_upload(
        self,
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> UUID:
        """
        Uploads document for applicant using sdk token.
        Use DocumentType with side DocumentType.IdCardFront for example
        or pass document_side parameter.
        """
        return await self._upload("sdk", document_type, file, document_side)

    @staticmethod
    async def __get_document(response: ClientResponse) -> Document:
        content_type = response.headers.get("Content-Type")
        try:
            document_type = DocumentType(response.headers.get("X-Document-Type"))
        except ValueError:
            document_type = None
        content = await response.read()
        return Document(content=content, content_type=content_type, document_type=document_type)

    @validate_arguments
    async def download(self, document_id: UUID) -> Document:
        async with self._session.get(url=f"{self._api_endpoint}/api/v3/documents/{document_id}") as response:
            await self._validate_resp(response, [200], "download document")
            return await self.__get_document(response)

    @validate_arguments
    async def download_preview(self, document_id: UUID) -> Document:
        async with self._session.get(url=f"{self._api_endpoint}/api/v3/documents/{document_id}/preview") as response:
            await self._validate_resp(response, [200], "download document preview")
            return await self.__get_document(response)
