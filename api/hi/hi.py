import logging
import random
import time

from flask import Blueprint

from uitls.restful import JsonRes
from uitls.log import log_request

bp = Blueprint('hi', __name__, url_prefix="/hi")

LOG = logging.getLogger(__name__)


@bp.route('/', methods=['GET'])
@log_request()
def hello():
    return JsonRes(200, True, {'hi': 'hi'})


@bp.route('/deal_task', methods=['GET'])
@log_request()
def deal_task():
    a = random.randrange(5, 10)
    print(f"任务执行 {a}s")
    time.sleep(a)
    return JsonRes(200, True, {'success': True})
