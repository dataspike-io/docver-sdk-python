from typing import Optional
from pydantic import validate_arguments
from requests import Response
from uuid import UUID
from model import DocumentSide, DocumentType
from ..resource import Resource


class Documents(Resource):
    def _upload(
        self,
        applicant_id: UUID,
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> Response:
        return self._session.post(
            url=f"{self._api_endpoint}/api/v3/upload/{applicant_id}",
            headers={"Content-Type": None},
            files={"file": ("file", file, "image/*")},
            data={"document_type": document_type, "side": document_side},
            timeout=self._timeout,
        )

    @validate_arguments
    def upload(
        self,
        applicant_id: UUID,
        document_type: DocumentType,
        file,
        document_side: Optional[DocumentSide] = None,
    ) -> UUID:
        response = self._upload(applicant_id, document_type, file, document_side)
        self._assert_resp(response, [200, 201], "upload document")
        data = response.json()
        return UUID(data["document_id"])
