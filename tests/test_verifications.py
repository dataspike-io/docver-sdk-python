from uuid import uuid4

from conftest import to_json
from dataspike import Api, Verification, CheckType, PagedResponse


async def test_verification_get(aioresponses, verification, api: Api):
    body = to_json(verification)

    aioresponses.get(f"{api.api_endpoint}/api/v3/verifications/{verification.id}", body=body)

    got = await api.verification.get(verification.id)
    aioresponses.assert_called_once()
    assert got == verification


async def test_verification_get_returns_none(aioresponses, api: Api):
    vid = uuid4()

    aioresponses.get(f"{api.api_endpoint}/api/v3/verifications/{vid}", status=404)

    got = await api.verification.get(vid)
    aioresponses.assert_called_once()
    assert got is None


async def test_verification_proceed(aioresponses, api: Api):
    v_id = uuid4()
    aioresponses.post(f"{api.api_endpoint}/api/v3/verifications/{v_id}/proceed")

    await api.verification.proceed(v_id)
    aioresponses.assert_called_once()


async def test_verification_create(aioresponses, verification, api: Api):
    aioresponses.post(f"{api.api_endpoint}/api/v3/verifications", status=201, body=to_json(verification))
    applicant_id = uuid4()
    resp = await api.verification.create(checks=[CheckType.Passport], applicant_id=applicant_id)
    aioresponses.assert_called_once()
    assert resp == verification


async def test_verification_list(aioresponses, verification, api: Api):
    data = PagedResponse[Verification](data=[verification], has_next=False)
    aioresponses.get(
        r"https://api.dataspike.io/api/v3/verifications?page=0&limit=10",
        status=200,
        body=to_json(data),
    )

    got = await api.verification.list()
    aioresponses.assert_called_once()
    assert list(got.data) == list(data.data)
    assert got.has_next == data.has_next


async def test_verification_list_for_applicant(aioresponses, verification, api: Api):
    data = PagedResponse[Verification](data=[verification], has_next=False)
    applicant_id = uuid4()
    aioresponses.get(
        f"https://api.dataspike.io/api/v3/verifications/applicant/{applicant_id}?page=0&limit=10",
        status=200,
        body=to_json(data),
    )

    got = await api.verification.list_for_applicant(applicant_id)
    aioresponses.assert_called_once()
    assert list(got.data) == list(data.data)
    assert got.has_next == data.has_next
