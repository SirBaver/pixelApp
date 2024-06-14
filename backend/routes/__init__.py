from flask import Flask, request, g
from extensions import db, mail_instance, babel, cors
import logging
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['BABEL_DEFAULT_LOCALE'] = os.getenv('BABEL_DEFAULT_LOCALE')
    app.config['BABEL_SUPPORTED_LOCALES'] = os.getenv('BABEL_SUPPORTED_LOCALES').split(',')
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.getenv('BABEL_TRANSLATION_DIRECTORIES')

    db.init_app(app)
    mail_instance.init_app(app)
    babel.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:8100"}})  # Configurer CORS pour toutes les routes

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from routes.session import session_bp
    app.register_blueprint(session_bp, url_prefix='/session')

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
