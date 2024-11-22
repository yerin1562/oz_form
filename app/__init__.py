# 초기화
# 패키지화

import click
from config import api, db
from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from app.routes import bp as main_bp  # 블루프린트 임포트
import app.models

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    app.secret_key = "oz_form_secret"
    

        # app.config 
    app.config['WTF_CSRF_ENABLED'] = False

    app.config['API_TITLE'] = 'oz_form'
    app.config['API_VERSION'] = '1.0'
    app.config['OPENAPI_VERSION'] = '3.1.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    db.init_app(app)
    api.init_app(app)

    migrate.init_app(app, db)


    # 블루 프린트 등록
    app.register_blueprint(main_bp)

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.create_all()
        click.echo("Initialized the database.")

    app.cli.add_command(init_db_command)

    return app
