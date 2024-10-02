import sys
import json
from uuid import UUID
from datetime import datetime
from .common import PagedResponse
import dataclasses

if sys.version_info >= (3, 11, 0):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class DataspikeJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, PagedResponse):
            return {"data": list(o.data), "has_next": o.has_next}
        elif dataclasses.is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        elif hasattr(o, "__iter__"):
            return list(o)  # type: ignore[attr-defined] # wait when pyright will be smarter
        else:
            return super().default(o)
