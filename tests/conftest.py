import asyncio
import dataclasses
import json
import pathlib
import sys
from uuid import UUID, uuid4
from datetime import datetime

import pytest
import pytest_asyncio

try:
    from dataspike import Api
except ImportError:
    rootdir = pathlib.Path(__file__).parent.parent.resolve().as_posix()
    sys.path.insert(0, rootdir)
    from dataspike import Api

from dataspike import *


class ResponseJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, PagedResponse):
            return {"data": list(obj.data), "has_next": obj.has_next}
        elif dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return dataclasses.asdict(obj)
        else:
            return super().default(obj)


def to_json(obj) -> str:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return json.dumps(dataclasses.asdict(obj), cls=ResponseJsonEncoder)
    return json.dumps(obj, cls=ResponseJsonEncoder)


@pytest_asyncio.fixture
async def api():
    async with Api("token1") as client:
        yield client


@pytest.fixture
def syncapi():
    with SyncApi("token_sync") as client:
        yield client


def pytest_collection_modifyitems(config, items):
    for item in items:
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)


@pytest.fixture
def verification() -> Verification:
    return Verification(
        id=uuid4(),
        applicant_id=uuid4(),
        status=VerificationStatus.Verified,
        organization_id="org_123",
        account_id="api",
        account_email="api@api.api",
        created_at=datetime.now(),
        checks=Checks(
            document_mrz=CheckResult(status=CheckStatus.Verified, data={"mrz": {"name": "John"}}),
            document_ocr=CheckResult(status=CheckStatus.Verified),
            face_comparison=CheckResult(status=CheckStatus.Verified),
            poa=CheckResult(status=CheckStatus.Verified),
        ),
        completed_at=datetime.now(),
        documents=[
            DocumentRef(document_id=uuid4(), document_type=DocumentType.Passport),
            DocumentRef(document_id=uuid4(), document_type=DocumentType.Selfie),
            DocumentRef(document_id=uuid4(), document_type=DocumentType.Poa),
        ],
        document_type=DocumentType.Passport,
    )
