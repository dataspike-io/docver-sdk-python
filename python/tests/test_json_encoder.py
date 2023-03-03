import json
from typing import Any
from dataspike import CheckType
from dataspike.utils import DataspikeJsonEncoder


def json_dumps(obj: Any) -> str:
    return json.dumps(obj, cls=DataspikeJsonEncoder)


def test_encode_iterator():
    data = [CheckType.Passport, CheckType.Selfie]
    it = iter(data)
    result = json_dumps(it)
    given = json.loads(result)
    assert given == data


def test_encode_tuple():
    data = (CheckType.Passport, CheckType.Selfie)
    result = json_dumps(data)
    given = json.loads(result)
    assert given == list(data)
