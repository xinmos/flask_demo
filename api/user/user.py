import logging

from flask import Blueprint

from service.user import UserService
from uitls.restful import JsonRes
from uitls.log import log_request

bp = Blueprint('user', __name__, url_prefix="/user")

LOG = logging.getLogger(__name__)


@bp.route('/get', methods=['GET'])
@log_request()
def get_user():
    user = UserService.query_by_id(1)
    return JsonRes(200, True, user)
