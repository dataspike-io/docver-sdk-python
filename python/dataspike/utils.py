import sys


if sys.version_info >= (3, 11, 0):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        pass
