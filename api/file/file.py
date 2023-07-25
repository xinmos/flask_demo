import os

from flask import Blueprint, request

from uitls.restful import JsonRes
from uitls.log import log_request

bp = Blueprint('file', __name__, url_prefix="/file")


@bp.route('/upload/accept', methods=['POST'])
@log_request()
def upload():
    upload_file = request.files['file']
    task = request.form.get('task_id')
    chunk = request.form.get('chunk', 0)
    filename = '%s%s' % (task, chunk)
    upload_file.save('./upload/%s' % filename)

    return JsonRes(200, True, {'filename': filename})


@bp.route("/upload/complete", methods=['GET'])
@log_request()
def upload_complete():
    target_filename = request.args.get('filename')
    task = request.args.get('task_id')
    chunk = 0
    with open('./upload/%s' % target_filename, 'wb') as target_file:
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'rb')
                target_file.write(source_file.read())
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)

    return JsonRes(200, True)
