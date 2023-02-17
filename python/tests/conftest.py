import pathlib
import sys
import pytest_asyncio

try:
    from dataspike import Api
except ImportError:
    rootdir = pathlib.Path(__file__).parent.parent.resolve().as_posix()
    sys.path.insert(0, rootdir)
    from dataspike import Api



@pytest_asyncio.fixture
async def api():
    async with Api("token1") as client:
        yield client
