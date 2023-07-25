import logging
import os
import time
from functools import wraps

from flask import request
from pythonjsonlogger import jsonlogger

JSON_LOG_FORMATTER = "%(appName)s %(service)s %(asctime)s %(levelname)s %(message)s %(request)s %(response)s %(rt)s"


class JSONFilter(logging.Filter):
    rt = 0
    appName = "myapp"
    response = {}

    def request_parse(self):
        params = {}
        if request.method == "GET":
            params = request.args.to_dict()
        elif request.method == "POST" or request.method == "PUT":
            if request.form:
                params = request.form.to_dict()
            else:
                params = request.get_json()
        return params

    def filter(self, record):
        record.message = record.msg
        record.service = f"{request.method} {request.path}"
        record.appName = self.appName
        record.rt = self.rt
        record.request = self.request_parse()
        record.response = self.response
        return True


def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def set_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = jsonlogger.JsonFormatter(JSON_LOG_FORMATTER)

    json_filter = JSONFilter()
    logger.addFilter(json_filter)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    log_path = make_dirs("./logs")
    file_handler = logging.FileHandler(os.path.join(log_path, f"{name}.log"))
    file_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(file_handler)

    return logger


monitor_logger = set_logger("monitor")


def log_request():
    def decor(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            _filter = monitor_logger.filters[0]

            start_time = time.time()
            response = func(*args, **kwargs)
            _filter.rt = round(time.time() - start_time, 3)
            _filter.response = response.json
            monitor_logger.info("")

            return response
        return wrapped
    return decor
