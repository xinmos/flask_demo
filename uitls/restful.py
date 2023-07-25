import datetime
import json

from flask import Response

_SIMPLE_TYPE = (str, int, type(None), bool, float)


def json_encoder(value):
    if isinstance(value, _SIMPLE_TYPE):
        return value
    if isinstance(value, datetime.datetime):
        return value.isoformat() + "Z"
    elif isinstance(value, Exception):
        return {
            "exception": value.__class__.__name__,
            "message": str(value)
        }


class JsonRes(Response):
    def __init__(self, code=200, status=True, data=None, error=None):
        self.res = {
            'code': code,
            'status': status,
        }
        if data is not None:
            self.res['data'] = data
        if error is not None:
            self.res['error'] = error

        content = json.dumps(self.res, default=json_encoder)
        try:
            super().__init__(content, status=code, mimetype="application/json")
        except TypeError:
            super(JsonRes, self).__init__(content, status=code, mimetype="application/json")
