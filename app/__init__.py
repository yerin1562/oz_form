# 초기화
# 패키지화

import click
from config import api, db
from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from app.routes_.question import question_bp
from app.routes_.answer import answer_bp
from app.routes_.users import user_bp
from app.routes_.detail_questions import detail_questions_bp 
from app.routes_ import index_bp


import app.models

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app = Flask(__name__)

    app.config.from_object("config.Config")
    app.secret_key = "oz_form_secret"
    app.config.from_object("config.Config")
    app.secret_key = "oz_form_secret"

        # app.config 

    app.config['API_TITLE'] = 'oz_form'
    app.config['API_VERSION'] = '1.0'
    app.config['OPENAPI_VERSION'] = '3.1.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWQGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    db.init_app(app)
    api.init_app(app)

    migrate.init_app(app, db)


    # question 블루 프린트 등록
    app.register_blueprint(question_bp)
    app.register_blueprint(answer_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(detail_questions_bp)
    app.register_blueprint(index_bp)


    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.create_all()
        click.echo("Initialized the database.")

    app.cli.add_command(init_db_command)

    return app
