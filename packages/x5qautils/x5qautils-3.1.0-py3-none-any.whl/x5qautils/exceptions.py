import json
import logging

from .helpers import attach_json

log = logging.getLogger('testing')


class AuthError(Exception):
    """
    Не прошла авторизация
    """
    pass


class StatusCodeError(AssertionError):
    """
    Статус код ответа не соотвествует 200-ым или не из переданных в `valid_status_codes` - для QaSession
    """

    def __init__(self, msg, response_msg, *args):
        self.response_msg = response_msg
        attach_json(response_msg, 'Error response')
        log.error(msg)
        super().__init__(msg, *args)


class SectionLoadError(AssertionError):
    """
    Не загрузился блок/секция
    """
    pass


class JSONValidationError(AssertionError):
    """
    Не валидный json
    """

    def __init__(self, msg, *args):
        log.error(msg)
        super().__init__(msg, *args)


class DiffError(AssertionError):
    """
    Данные не сошлись
    """

    def __init__(self, message='', diff=None):
        attach = json.dumps(diff, indent=4, ensure_ascii=False)

        attach_json(attach, name='Diff')
        log.info('Diff: /n/t%s', attach)
        super().__init__(message or 'Данные не сошлись')
