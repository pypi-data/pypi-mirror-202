import logging
from functools import wraps

from furl import furl

from ..helpers import dumps


def log_request(f):
    @wraps(f)
    def wrapper(self, method, url, *args, params=None, headers=None, data=None, json=None, **kwargs):
        _url = furl(url, query_params=params)
        _headers = '-H '.join(f'"{k}: {v}"' for k, v in headers.items()) if headers else ''
        _data = f'-d "{data or dumps(json, ensure_ascii=False)}"' if data or json else ''
        log.info('curl -X %s %s %s %s', method, _url, _headers, _data)
        return f(self, method, url, *args, params=params, headers=headers, data=data, json=json, **kwargs)

    return wrapper


log = logging.getLogger('API')
