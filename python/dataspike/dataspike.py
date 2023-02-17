from typing import TYPE_CHECKING, Optional

import requests

from .applicants.resource import Applicants
from .documents.resource import Documents
from .sdk.resource import Sdk
from .verifications.resource import Verifications
from .resource import _TIMEOUT_TPE

try:
    import pkg_resources
    CURRENT_VERSION = pkg_resources.get_distribution("dataspike-python").version
except ImportError:
    CURRENT_VERSION = "dev"

class Api:

    def __init__(self, api_token: str, api_endpoint: str = "https://api.dataspike.io", timeout: Optional[_TIMEOUT_TPE] = None):
        self._api_endpoint = api_endpoint
        session = requests.Session()
        default_headers = {"ds-api-token": api_token,
                 "Content-Type": "application/json",
                 "User-Agent": f"dataspike-python/{CURRENT_VERSION}",
                 }
        session.headers.update(default_headers)
        self.applicant = Applicants(session, api_endpoint, timeout)
        self.verification = Verifications(session, api_endpoint, timeout)
        self.document = Documents(session, api_endpoint, timeout)
        self.sdk = Sdk(session, api_endpoint, timeout)

    def __repr__(self) -> str:
        return f"DataspikeApi<{self._api_endpoint}>"

