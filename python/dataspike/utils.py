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
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, PagedResponse):
            return {"data": list(obj.data), "has_next": obj.has_next}
        elif dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return dataclasses.asdict(obj)
        elif hasattr(obj, "__iter__"):
            return list(obj)  # type: ignore[attr-defined] # wait when pyright will be smarter
        else:
            return super().default(obj)
