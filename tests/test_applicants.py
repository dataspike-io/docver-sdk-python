from uuid import UUID

from conftest import to_json
from dataspike import Applicant, ApplicantInfo, Api, PagedResponse


async def test_applicant_get(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)
    applicant = Applicant(applicant_id=applicant_id, system_info=ApplicantInfo(full_name="John Doe"))
    body = to_json(applicant)

    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/{applicant_id}", body=body)

    got = await api.applicant.get(applicant_id)
    aioresponses.assert_called_once()
    assert got == applicant


async def test_applicant_get_return_none(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)
    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/{applicant_id}", status=404)

    got = await api.applicant.get(applicant_id)
    aioresponses.assert_called_once()
    assert got is None


async def test_applicant_get_by_external_id(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)
    external_id = "asd1"
    applicant = Applicant(
        applicant_id=applicant_id, external_id=external_id, system_info=ApplicantInfo(full_name="John Doe")
    )
    body = to_json(applicant)

    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/by_external_id/{external_id}", body=body)

    got = await api.applicant.get_by_external_id(external_id)
    aioresponses.assert_called_once()
    assert got == applicant


async def test_applicant_create(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524467342344623421465345)
    url = "https://api.dataspike.io/api/v3/applicants"
    response_body = to_json({"id": str(applicant_id)})
    aioresponses.post(url, status=201, body=response_body)

    got = await api.applicant.create("ex_id1")
    aioresponses.assert_called_once_with(url, "POST", json={"external_id": "ex_id1"})
    assert got == applicant_id


async def test_applicant_list(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524467342344623421465345)
    applicant = Applicant(applicant_id=applicant_id, system_info=ApplicantInfo(full_name="John Doe"))
    data = PagedResponse[Applicant](data=[applicant], has_next=False)
    aioresponses.get(
        r"https://api.dataspike.io/api/v3/applicants?page=0&limit=10",
        status=200,
        body=to_json(data),
    )

    got = await api.applicant.list()
    aioresponses.assert_called_once()
    assert list(got.data) == list(data.data)
    assert got.has_next == data.has_next


async def test_applicant_delete(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)
    url = f"https://api.dataspike.io/api/v3/applicants/{applicant_id}"
    aioresponses.delete(url)

    await api.applicant.delete(applicant_id)
    aioresponses.assert_called_once_with(url, "DELETE")
