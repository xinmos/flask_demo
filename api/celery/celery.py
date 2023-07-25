from flask import Blueprint, request

from uitls import tasks
from uitls.restful import JsonRes
from uitls.log import log_request

bp = Blueprint('celery', __name__, url_prefix="/celery")


@bp.route('/test1', methods=['GET'])
@log_request()
def test1():
    task = tasks.test1.delay(1, 2)
    return JsonRes(200, True, {"task_id": task.id})


@bp.route('/test1/status', methods=['POST'])
@log_request()
def test1_status():
    params = request.get_json()
    task = tasks.test1.AsyncResult(task_id=params['task_id'])
    if task.status == 'SUCCESS':
        result = task.result
        return JsonRes(200, True, {"result": result})
    else:
        return JsonRes(200, False, {"status": task.status})
