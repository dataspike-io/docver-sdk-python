from types import TracebackType
from typing import Optional, Type

from aiohttp import ClientSession

from .applicants.applicants import Applicants
from .documents.documents import Documents
from .sdk.sdk import Sdk
from .verifications.verifications import Verifications

try:
    import pkg_resources

    try:
        CURRENT_VERSION = pkg_resources.get_distribution("dataspike-python").version
    except pkg_resources.DistributionNotFound:
        CURRENT_VERSION = "dev"
except ImportError:
    CURRENT_VERSION = "dev"


class Api:
    def __init__(self, api_token: str, api_endpoint: str = "https://api.dataspike.io", **kwargs):
        """
        :param api_token: Organization API token
        :param api_endpoint: API endpoint, default "https://api.dataspike.io"
        :param kwargs: aiottp.ClientSession params, pass here timeouts or other options
        """
        self._api_endpoint = api_endpoint
        self._session = ClientSession(**kwargs)
        default_headers = {
            "ds-api-token": api_token,
            "Content-Type": "application/json",
            "User-Agent": f"dataspike-python/{CURRENT_VERSION}",
        }
        self._session.headers.update(default_headers)
        self.applicant: Applicants = Applicants(self._session, api_endpoint)
        self.verification = Verifications(self._session, api_endpoint)
        self.document = Documents(self._session, api_endpoint)
        self.sdk = Sdk(self._session, api_endpoint)

    def __repr__(self) -> str:
        return f"DataspikeApi<{self._api_endpoint}>"

    def __enter__(self) -> None:
        raise TypeError("Use async with instead")

    async def __aenter__(self) -> "Api":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self):
        await self._session.close()
