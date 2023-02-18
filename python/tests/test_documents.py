from uuid import UUID
from dataspike import Api, DocumentType
from conftest import to_json


async def test_document_upload(aioresponses, api: Api):
    applicant_id = UUID(int=24625621345245)
    doc_id = UUID(int=64724769385623)
    aioresponses.post(f"{api.api_endpoint}/api/v3/upload/{applicant_id}", body=to_json({"document_id": doc_id}))
    with open(__file__, "r") as f:
        got = await api.document.upload(applicant_id, DocumentType.Passport, f)
        assert got == doc_id
    aioresponses.assert_called_once()
