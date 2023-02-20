from typing import Iterable

from aiohttp import ClientResponse, ClientSession

from .errors import UnexpectedResponseStatus


class Resource:
    def __init__(self, session: ClientSession, api_endpoint: str):
        self._api_endpoint = api_endpoint
        self._session = session

    @classmethod
    async def _validate_resp(cls, response: ClientResponse, statuses: Iterable[int], method: str) -> None:
        if response.status not in statuses:
            expected = ", ".join(str(i) for i in statuses)
            response_text = await response.text()
            raise UnexpectedResponseStatus(
                method,
                response.status,
                response_text,
                f"{method} failed, expected {expected} " f"got {response.status}, response {response_text}",
            )
