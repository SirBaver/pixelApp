# backend/routes/__init__.py
from flask import Flask, request, g
from extensions import db, mail_instance, babel, cors
import logging
import os

logging.basicConfig(level=logging.DEBUG)

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
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(os.path.dirname(__file__), '..', 'translations')

    db.init_app(app)
    mail_instance.init_app(app)
    babel.init_app(app)
    cors.init_app(app, resources={r"/auth/*": {"origins": "http://localhost:8100"}})  # Configurer CORS pour les routes d'authentification

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    def get_locale():
        user = getattr(g, 'user', None)
        if user is not None:
            logging.debug(f"Preferred language of user: {user.preferred_language}")
            return user.preferred_language
        locale = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
        logging.debug(f"Best matched locale: {locale}")
        return locale

    babel.locale_selector_func = get_locale

    logging.debug(f"Babel configuration: {app.config['BABEL_SUPPORTED_LOCALES']}, {app.config['BABEL_TRANSLATION_DIRECTORIES']}")

    # Ajout de journaux pour vérifier le chargement des fichiers de traduction
    for locale in app.config['BABEL_SUPPORTED_LOCALES']:
        logging.debug(f"Loading translations for locale: {locale}")
        translations_path = os.path.join(app.config['BABEL_TRANSLATION_DIRECTORIES'], locale, 'LC_MESSAGES', 'messages.mo')
        if os.path.exists(translations_path):
            logging.debug(f"Found translations file: {translations_path}")
        else:
            logging.debug(f"Translations file not found: {translations_path}")

    return app
