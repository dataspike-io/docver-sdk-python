from typing import Optional

from requests import Response

from ..documents import DocumentType, DocumentSide
from ..resource import Resource
from pydantic import validate_arguments
from uuid import UUID


class Sdk(Resource):

    def _create_token(self, applicant_id) -> Response:
        return self._session.post(
            url=f"{self._api_endpoint}/api/v3/sdk_token",
            json={"applicant_id": str(applicant_id)},
            timeout=self._timeout
        )

    @validate_arguments
    def create_token(self, applicant_id: UUID) -> str:
        response = self._create_token(applicant_id)
        self._assert_resp(response, [200, 201], "sdk token create")
        data = response.json()
        return data['token']

    @validate_arguments
    def _upload_document(self, sdk_token: str, document_type: DocumentType, file,
                         document_side: Optional[DocumentSide] = None) -> UUID:
        response = self._session.post(
            url=f"{self._api_endpoint}/api/v3/upload/sdk",
            headers={
                'Content-Type': None,
                "ds-api-token": sdk_token
            },
            files={"file": ("file", file, "image/*")},
            data={"document_type": document_type, "side": document_side},
            timeout=self._timeout
        )
        self._assert_resp(response, [200, 201], "sdk upload file")
        data = response.json()
        return UUID(data['document_id'])
