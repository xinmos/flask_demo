from celery import Celery
from flask import Flask, Blueprint
from flask_cors import CORS

from api.file.file import bp as file_bp
from api.hi.hi import bp as hi_bp
from api.celery.celery import bp as celery_bp
from api.user.user import bp as user_bp
from uitls.database import db


def celery_init_app(app):
    celery_app = Celery(app.name)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/1",
            task_ignore_result=True,
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json'
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    sql_config = {
        "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://root:root@localhost:3306/flask_demo?charset=utf8",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_ECHO": False,
        "SQLALCHEMY_POOL_SIZE": 10,
        "SQLALCHEMY_POOL_TIMEOUT": 60,
        "SQLALCHEMY_POOL_RECYCLE": 600
    }
    app.config.update(sql_config)

    app_bp = Blueprint('api', __name__, url_prefix='/api')
    app_bp.register_blueprint(file_bp)
    app_bp.register_blueprint(hi_bp)
    app_bp.register_blueprint(celery_bp)
    app_bp.register_blueprint(user_bp)
    app.register_blueprint(app_bp)

    db.init_app(app)

    return app
