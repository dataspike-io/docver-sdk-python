from uuid import UUID
from dataspike import Api, DocumentType, Document
from conftest import to_json


async def test_document_upload(aioresponses, api: Api):
    applicant_id = UUID(int=24625621345245)
    doc_id = UUID(int=64724769385623)
    aioresponses.post(f"{api.api_endpoint}/api/v3/upload/{applicant_id}", body=to_json({"document_id": doc_id}))
    f = b"asdasd"
    got = await api.document.upload(applicant_id, DocumentType.Passport, f)
    assert got == doc_id
    aioresponses.assert_called_once()


async def test_document_download(aioresponses, api: Api):
    doc_id = UUID(int=6472476938565623)
    expected = Document(content=b"content_of_file", content_type="image/png", document_type=DocumentType.IdCardFront)
    aioresponses.get(
        f"{api.api_endpoint}/api/v3/documents/{doc_id}",
        body=expected.content,
        headers={"Content-Type": expected.content_type, "X-Document-Type": expected.document_type},
    )
    got = await api.document.download(doc_id)
    assert got == expected
    aioresponses.assert_called_once()


async def test_document_download_preview(aioresponses, api: Api):
    doc_id = UUID(int=6472476938565623)
    expected = Document(content=b"content_of_file", content_type="image/png", document_type=DocumentType.IdCardFront)
    aioresponses.get(
        f"{api.api_endpoint}/api/v3/documents/{doc_id}/preview",
        body=expected.content,
        headers={"Content-Type": expected.content_type, "X-Document-Type": expected.document_type},
    )
    got = await api.document.download_preview(doc_id)
    assert got == expected
    aioresponses.assert_called_once()
