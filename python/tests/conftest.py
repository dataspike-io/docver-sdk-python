import asyncio
import dataclasses
import json
import pathlib
import sys
from uuid import UUID

import pytest
import pytest_asyncio

try:
    from dataspike import Api
except ImportError:
    rootdir = pathlib.Path(__file__).parent.parent.resolve().as_posix()
    sys.path.insert(0, rootdir)
    from dataspike import Api

from dataspike import PagedResponse


class ResponseJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        match obj:
            case UUID():
                return str(obj)
            case PagedResponse():
                return {"data": obj.data, "has_next": obj.has_next}
            case x if dataclasses.is_dataclass(x) and not isinstance(obj, type):
                return dataclasses.asdict(obj)
            case _:
                return super().default(obj)


def to_json(obj) -> str:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return json.dumps(dataclasses.asdict(obj), cls=ResponseJsonEncoder)
    return json.dumps(obj, cls=ResponseJsonEncoder)


@pytest_asyncio.fixture
async def api():
    async with Api("token1") as client:
        yield client


def pytest_collection_modifyitems(config, items):
    for item in items:
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)
