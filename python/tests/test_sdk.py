from uuid import uuid4

from conftest import to_json
from dataspike import Api


async def test_sdk_create_token(aioresponses, api: Api):
    applicant_id = uuid4()
    expected = 'expected_token"'
    aioresponses.post(f"{api.api_endpoint}/api/v3/sdk_token", body=to_json({"token": expected}))

    got = await api.sdk.create_token(applicant_id)
    aioresponses.assert_called_once()
    assert got == expected
