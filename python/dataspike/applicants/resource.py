import dataclasses

from requests import Response
from pydantic import validate_arguments
from ..resource import Resource
from ..common import *
from model import *
from uuid import UUID


class Applicants(Resource):
    def _get(self, applicant_id: UUID) -> Response:
        return self._session.get(
            url=f"{self._api_endpoint}/api/v3/applicants/{applicant_id}",
            timeout=self._timeout,
        )

    @validate_arguments
    def get(self, applicant_id: UUID) -> Applicant:
        response = self._get(applicant_id)
        assert (
            response.status_code == 200
        ), f"get applicant failed, expected 200 got {response.status_code}, body: {response.text}"
        data = response.json()
        return Applicant(**data)

    @validate_arguments
    def find(self, applicant_id: UUID) -> Optional[Applicant]:
        response = self._get(applicant_id)
        if response.status_code == 404:
            return None
        assert (
            response.status_code == 200
        ), f"get applicant failed, expected 200 got {response.status_code}, body: {response.text}"
        data = response.json()
        return Applicant(**data)

    def _create(
        self, external_id: Optional[str] = None, info: Optional[ApplicantInfo] = None
    ) -> Response:
        body = {}
        if external_id is not None:
            body["external_id"] = external_id
        if info is not None:
            body["info"] = dataclasses.asdict(info)
        return self._session.post(
            url=f"{self._api_endpoint}/api/v3/applicants",
            json=body,
            timeout=self._timeout,
        )

    @validate_arguments
    def create(
        self, external_id: Optional[str] = None, info: Optional[ApplicantInfo] = None
    ) -> UUID:
        response = self._create(external_id, info)

        assert (
            response.status_code == 201
        ), f"create applicant failed, expected 201 got {response.status_code}, body: {response.text}"

        data = response.json()
        return UUID(data["id"])

    def _list(self, page: int = 0, limit: int = 10) -> Response:
        return self._session.get(
            url=f"{self._api_endpoint}/api/v3/applicants?page={page}&?limit={limit}",
            timeout=self._timeout,
        )

    @validate_arguments
    def list(self, page: int = 0, limit: int = 10) -> PagedResponse[Applicant]:
        response = self._list(page, limit)
        assert (
            response.status_code == 200
        ), f"list applicants failed, expected 200 got {response.status_code}, response {response.text}"
        data = response.json()
        return PagedResponse[Applicant](**data)

    def _delete(self, applicant_id: UUID) -> Response:
        return self._session.delete(
            url=f"{self._api_endpoint}/api/v3/applicants/{applicant_id}",
            timeout=self._timeout,
        )

    @validate_arguments
    def delete(self, applicant_id: UUID) -> None:
        response = self._delete(applicant_id)
        assert (
            response.status_code == 200
        ), f"delete applicant failed, expected 200 got {response.status_code}, response {response.text}"
