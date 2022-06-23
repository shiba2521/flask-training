from flask import Flask
from flask_login import LoginManager
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

csrf = CSRFProtect()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""

def create_app(config_key):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="ABCD1234",
        SQLALCHEMY_DATABASE_URI= f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="NDIJWNDiendw",
    )

    db.init_app(app)
    csrf.init_app(app)

    Migrate(app, db)
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.config.from_object(config[config_key])

    login_manager.init_app(app)

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.detector import views as dt_views

    #viewsのdtをアプリへ登録
    app.register_blueprint(dt_views.dt)
    
    return app

    