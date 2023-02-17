import pytest
from uuid import UUID
import json
from dataspike import Applicant, ApplicantInfo
import dataclasses


class ResponseJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return super().default(obj)


@pytest.mark.asyncio
async def test_something(aioresponses, api):
    id = UUID(int=21355515246424524622342344623421465345)
    applicant = Applicant(applicant_id=id, display_info=ApplicantInfo(full_name="John Doe"))
    body = json.dumps(dataclasses.asdict(applicant), cls=ResponseJsonEncoder)

    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/{id}", body=body)

    got = await api.applicant.get(id)
    assert got == applicant

