from uuid import uuid4

from conftest import to_json
from dataspike import Api, Verification, DocumentType


async def test_verification_get(aioresponses, verification, api: Api):
    body = to_json(verification)

    aioresponses.get(f"{api.api_endpoint}/api/v3/verifications/{verification.id}", body=body)

    got: Verification = await api.verification.get(verification.id)
    aioresponses.assert_called_once()
    assert got == verification


async def test_verification_find(aioresponses, verification, api: Api):
    body = to_json(verification)

    aioresponses.get(f"{api.api_endpoint}/api/v3/verifications/{verification.id}", body=body)

    got = await api.verification.find(verification.id)
    aioresponses.assert_called_once()
    assert got == verification


async def test_verification_find_returns_none(aioresponses, api: Api):
    vid = uuid4()

    aioresponses.get(f"{api.api_endpoint}/api/v3/verifications/{vid}", status=404)

    got = await api.verification.find(vid)
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
    resp = await api.verification.create(checks_required=[DocumentType.Passport], applicant_id=applicant_id)
    aioresponses.assert_called_once()
    assert resp == verification
