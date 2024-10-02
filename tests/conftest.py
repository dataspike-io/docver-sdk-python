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
from dataspike.verifications.model import PoiData


class ResponseJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, PagedResponse):
            return {"data": list(o.data), "has_next": o.has_next}
        elif dataclasses.is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        else:
            return super().default(o)


def to_json(obj) -> str:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return json.dumps(dataclasses.asdict(obj), cls=ResponseJsonEncoder)
    return json.dumps(obj, cls=ResponseJsonEncoder)


@pytest_asyncio.fixture
async def api():
    async with Api("token1") as client:
        yield client


@pytest.fixture
def sync():
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
        is_sandbox=False,
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
        poi_data=PoiData(name="John"),
        document_type=DocumentType.Passport,
    )
