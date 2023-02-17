from typing import Any, Optional, Iterable
from uuid import UUID
from requests import Session, Response

_TIMEOUT_TPE = float | tuple[float, float] | tuple[float, None]

class Resource:
    def __init__(self, session: Session, api_endpoint: str, timeout: Optional[_TIMEOUT_TPE]):
        self._api_endpoint = api_endpoint
        self._session = session
        self._timeout = timeout

    @staticmethod
    def _uuid_ids(data: dict[str, Any], *keys: str):
        for k in keys:
            data[k] = UUID(data[k])
        return data

    @classmethod
    def _assert_resp(cls, response: Response, statuses: Iterable[int], method: str):
        s = map(lambda i: str(i), statuses)
        assert response.status_code in statuses, \
            f"{method} failed, expected {', '.join(s)} got {response.status_code}, response {response.text}"
