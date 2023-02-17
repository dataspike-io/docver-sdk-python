from aiohttp import ClientSession

from .applicants.resource import Applicants
from .documents.resource import Documents
from .sdk.resource import Sdk
from .verifications.resource import Verifications

try:
    import pkg_resources

    CURRENT_VERSION = pkg_resources.get_distribution("dataspike-python").version
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
        session = ClientSession(**kwargs)
        default_headers = {
            "ds-api-token": api_token,
            "Content-Type": "application/json",
            "User-Agent": f"dataspike-python/{CURRENT_VERSION}",
        }
        session.headers.update(default_headers)
        self.applicant = Applicants(session, api_endpoint)
        self.verification = Verifications(session, api_endpoint)
        self.document = Documents(session, api_endpoint)
        self.sdk = Sdk(session, api_endpoint)

    def __repr__(self) -> str:
        return f"DataspikeApi<{self._api_endpoint}>"
