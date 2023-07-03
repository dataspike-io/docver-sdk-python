import json
from types import TracebackType
from typing import Optional, Type, Any

from aiohttp import ClientSession

from .applicants.applicants import Applicants
from .documents.documents import Documents
from .verifications.verifications import Verifications
from .aml.aml import AML
from .utils import DataspikeJsonEncoder

__all__ = ["Api"]

from .__version__ import __version__


class Api:
    @staticmethod
    def _encode_json(obj: Any) -> str:
        return json.dumps(obj, cls=DataspikeJsonEncoder)

    def __init__(self, api_token: str, api_endpoint: str = "https://api.dataspike.io", **kwargs):
        """
        :param api_token: Organization API token
        :param api_endpoint: API endpoint, default "https://api.dataspike.io"
        :param kwargs: aiottp.ClientSession params, pass here timeouts or other options
        """

        self.api_endpoint = api_endpoint
        default_headers = {
            "ds-api-token": api_token,
            "User-Agent": f"dataspike-python/{__version__}",
        }
        self._session = ClientSession(headers=default_headers, json_serialize=self._encode_json, **kwargs)
        self.applicant: Applicants = Applicants(self._session, api_endpoint)
        self.verification = Verifications(self._session, api_endpoint)
        self.document = Documents(self._session, api_endpoint)
        self.aml = AML(self._session, api_endpoint)

    def __repr__(self) -> str:
        return f"DataspikeApi<{self.api_endpoint}>"

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

    async def close(self) -> None:
        await self._session.close()
