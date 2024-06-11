# backend/routes/__init__.py
from flask import Flask, request, g
from extensions import db, mail_instance, babel
from flask_babel import Babel
from extensions import db  # Assurez-vous que le chemin d'importation est correct

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = '1234ABCD!'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 1025
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr', 'es']

    db.init_app(app)
    mail_instance.init_app(app)
    babel.init_app(app)

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    def get_locale():
        user = getattr(g, 'user', None)
        if user is not None:
            return user.preferred_language
        return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
    
    babel.locale_selector_func = get_locale

    return app

