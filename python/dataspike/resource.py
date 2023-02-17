from typing import Any, Iterable
from uuid import UUID

from aiohttp import ClientResponse, ClientSession

from .errors import UnexpectedResponseStatus


class Resource:
    def __init__(self, session: ClientSession, api_endpoint: str):
        self._api_endpoint = api_endpoint
        self._session = session

    @staticmethod
    def _uuid_ids(data: dict[str, Any], *keys: str):
        for k in keys:
            data[k] = UUID(data[k])
        return data

    @classmethod
    async def _validate_resp(cls, response: ClientResponse, statuses: Iterable[int], method: str) -> None:
        if response.status not in statuses:
            s = map(lambda i: str(i), statuses)
            response_text = await response.text()
            raise UnexpectedResponseStatus(
                method,
                response.status,
                response_text,
                f"{method} failed, expected {', '.join(s)} " f"got {response.status}, response {response_text}",
            )
