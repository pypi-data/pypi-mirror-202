import json
from contextlib import suppress
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from enum import Enum
from uuid import UUID

import allure
from pydantic import BaseModel


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, str):
            return obj
        return super().default(obj)


def dumps(obj, indent=4, ensure_ascii=False):
    if isinstance(obj, BaseModel):
        return obj.json(ensure_ascii=False)
    return json.dumps(
        obj,
        indent=indent,
        ensure_ascii=ensure_ascii,
        cls=CustomEncoder,
    )


def attach_json(obj, /, name=None):
    if not isinstance(obj, (str, bytes)):
        obj = dumps(obj, indent=4, ensure_ascii=False)
    with suppress(KeyError):
        allure.attach(obj, attachment_type=allure.attachment_type.JSON, name=name)


def to_json_valid(obj):
    if isinstance(obj, BaseModel):
        return json.loads(obj.json(by_alias=True, exclude_none=True))
    elif isinstance(obj, list):
        return [to_json_valid(v) for v in obj]
    elif is_dataclass(obj):
        return asdict(obj)
    elif isinstance(obj, dict):
        return {k: to_json_valid(v) for k, v in obj.items()}
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Enum):
        return obj.value
    return obj
