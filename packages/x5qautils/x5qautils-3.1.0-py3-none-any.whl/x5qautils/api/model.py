import re
from abc import ABC
from itertools import zip_longest
from typing import Any, List, Tuple, Union

import allure
import pydantic
from pydantic.dataclasses import dataclass

from ..exceptions import DiffError
from ..helpers import attach_json


def to_camel(string: str) -> str:
    words = string.split('_')
    return ''.join((words[0], *[word.capitalize() for word in words[1:]]))


def to_snake_case(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class NotSchemaValidator:
    @classmethod
    def schema_json(cls, *args, **kwargs):  # noqa
        return f'{{"Class {cls.__class__.__name__}": "Not schema validator"}}'


class BasePydantic(pydantic.BaseModel):
    @classmethod
    def init(cls, kwargs):
        with allure.step('Валидация модели (ответа)'):
            return cls.parse_obj(kwargs)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = pydantic.Extra.forbid


class BaseAPI(ABC, BasePydantic):
    def get(self, key, default=None):
        return self.__dict__.get(to_snake_case(key), default)

    def __getitem__(self, item):
        if getattr(self, '__root__', None):
            return self.__root__[item]
        return self.__dict__[to_snake_case(item)]

    def __iter__(self) -> str:
        yield from [key for key in self.__dict__ if not key.startswith('_')]

    def values(self) -> Tuple['BaseAPI']:
        yield from [self.__dict__[key] for key in self]

    def items(self) -> Tuple[str, 'BaseAPI']:
        yield from [(key, self.__dict__[key]) for key in self]

    @staticmethod
    def to_json_valid(value):
        if isinstance(value, (int, str, list, dict, bool, float)):
            return value
        if isinstance(value, BaseAPI):
            return value.dict()
        return str(value)

    def _compare(self, v, v_validation):
        if isinstance(v, BaseAPI):
            return v.difference(v_validation)
        if v_validation == '!not_empty' and not v:
            return {'Получили пустое значение': self.to_json_valid(v)}
        if v_validation == '!empty' and v:
            return {'Поулчили не пустое значение': self.to_json_valid(v)}
        if v_validation and not str(v_validation).startswith('!') and v != v_validation:
            return {'Хотели': self.to_json_valid(v_validation), 'Получили': self.to_json_valid(v)}
        return {}

    def difference(self, other: 'BaseAPI'):
        diff = {}
        with allure.step(f'Проверяем объект {self.__class__.__name__}'):
            attach_json(self.json(indent=4, exclude_none=True, ensure_ascii=False), 'Проверяемые объект')
            attach_json(other.json(indent=4, exclude_none=True, ensure_ascii=False), 'Валидация')
            for field, v in other.items():
                if isinstance(v_list := getattr(v, '__root__', v), list):
                    v_out_list = getattr(self[field], '__root__', self[field])
                    new_err = [
                        diff_
                        for v_in, v_out in zip_longest(v_out_list, v_list, fillvalue=BaseAPI())
                        if (diff_ := self._compare(v_in, v_out))
                    ]
                    if new_err:
                        diff[field] = new_err
                elif new_err := self._compare(self[field], v):
                    diff[field] = new_err
        return diff

    def is_validation(self, other: 'BaseAPI'):
        if diff := self.difference(other):
            raise DiffError(diff=diff)

    def equal(self, other: 'BaseAPI'):
        self.is_validation(other)

    def __contains__(self, other: 'BaseAPI'):
        assert not (diff := self.difference(other)), f'Diff {diff}'


class BaseListAPI(BaseAPI):
    """
    Model for lists of objects, attributes:
        * `_end_iterator` - number of end object for iterator
        * `_start_iterator` - number of start object for iterator
        * `_step_iterator` - number of step for iterator

    :param __root__ - type hints for responses. Example __root__: List[Photo]
    """
    _end_iterator = None
    _start_iterator = None
    _step_iterator = None

    def __iter__(self):
        yield from self.__root__[self._start_iterator:self._end_iterator:self._step_iterator]


class CodeError(BaseAPI):
    code: str = ''
    description: Union[str, tuple] = ''
    name: str = ''


class DictAPI(dict, NotSchemaValidator):
    @classmethod
    def init(cls, kw: dict):
        return cls(**kw)


class ListAPI(BasePydantic):
    __root__: List[Any]

    def get(self, index, default=None):
        try:
            return self.__root__[index]
        except IndexError:
            return default


class ByteAPI(bytes, NotSchemaValidator):
    @classmethod
    def init(cls, kw: dict):
        return cls(kw)


@dataclass
class BoolAPI(NotSchemaValidator):
    flag: bool = False

    @classmethod
    def init(cls, v):
        return cls(v)

    def __bool__(self):
        return self.flag
