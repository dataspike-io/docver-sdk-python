import asyncio
from copy import deepcopy
from functools import wraps

from .dataspike import Api
from .resource import Resource

__all__ = ["SyncApi"]


class SyncApi:
    __slots__ = ["applicant", "verification", "document", "aml", "sdk", "__loop", "__api"]

    @staticmethod
    async def __init_api(*args, **kwargs):
        return Api(*args, **kwargs)

    def __run(self, fn):
        return self.__loop.run_until_complete(fn)

    def __call(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return self.__run(fn(*args, **kwargs))

        return wrapper

    def __init__(self, *args, **kwargs):
        self.__loop = asyncio.get_event_loop()
        self.__api = self.__run(self.__init_api(*args, **kwargs))
        for attr in dir(self.__api):
            r = getattr(self.__api, attr)
            if not isinstance(r, Resource):
                continue
            holder = type(attr, (object,), {})()
            for n in dir(r):
                if n.startswith("_"):
                    continue
                m = getattr(r, n)
                c = m
                # it can be decorated with validated_arguments
                if hasattr(m, "raw_function"):
                    c = m.raw_function
                if not asyncio.iscoroutinefunction(c):
                    continue
                f = deepcopy(self.__call(m))
                setattr(holder, n, f)

            setattr(self, attr, holder)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"DataspikeSyncApi<{self.__api.api_endpoint}>"

    def close(self) -> None:
        asyncio.run(self.__api.close())
