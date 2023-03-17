from conftest import to_json
from uuid import UUID
from dataspike import Applicant, ApplicantInfo, SyncApi


def test_sync_applicant_get(aioresponses, syncapi: SyncApi):
    applicant_id = UUID(int=235135)
    applicant = Applicant(applicant_id=applicant_id, system_info=ApplicantInfo(full_name="John Doe"))
    body = to_json(applicant)

    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/{applicant_id}", body=body)

    got = syncapi.applicant.get(applicant_id)
    aioresponses.assert_called_once()
    assert got == applicant
