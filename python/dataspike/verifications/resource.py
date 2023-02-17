from typing import Any

from pydantic import validate_arguments
from requests import Response

from model import *
from ..documents.model import DocumentType
from ..resource import Resource


class Verifications(Resource):
    def _proceed(self, verification_id: UUID) -> Response:
        return self._session.post(
            url=f"{self._api_endpoint}/api/v3/verifications/{verification_id}/proceed",
            timeout=self._timeout,
        )

    @validate_arguments
    def proceed(self, verification_id: UUID) -> None:
        response = self._proceed(verification_id)
        self._assert_resp(response, [200], "proceed verification")

    def _create(
        self,
        checks_required: Sequence[DocumentType],
        applicant_id: Optional[UUID] = None,
    ) -> Response:
        body: dict[str, Any] = {"checks_required": checks_required}
        if applicant_id is not None:
            body["applicant_id"] = str(applicant_id)

        return self._session.post(
            url=f"{self._api_endpoint}/api/v3/verifications",
            json=body,
            timeout=self._timeout,
        )

    @validate_arguments
    def create(
        self,
        checks_required: Sequence[DocumentType],
        applicant_id: Optional[UUID] = None,
    ) -> Verification:
        response = self._create(checks_required, applicant_id)
        self._assert_resp(response, [201], "create verification")
        data = response.json()
        self._uuid_ids(data, "id", "applicant_id")

        return Verification(**data)

    def _get(self, verification_id: UUID) -> Response:
        return self._session.get(
            url=f"{self._api_endpoint}/api/v3/verifications/{verification_id}",
            timeout=self._timeout,
        )

    @validate_arguments
    def get(self, verification_id: UUID) -> Verification:
        response = self._get(verification_id)

        self._assert_resp(response, [200], "get verification")
        data = response.json()
        self._uuid_ids(data, "id", "applicant_id")
        return Verification(**data)

    @validate_arguments
    def find(self, verification_id: UUID) -> Optional[Verification]:
        response = self._get(verification_id)

        self._assert_resp(response, [200, 404], "find verification")
        if response.status_code == 404:
            return None
        data = response.json()
        self._uuid_ids(data, "id", "applicant_id")
        return Verification(**data)
