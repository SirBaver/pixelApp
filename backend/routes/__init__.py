from flask import Flask, request
from flask_babel import Babel, gettext, force_locale
from extensions import db, mail_instance, babel, cors, migrate
import os
from dotenv import load_dotenv

load_dotenv()

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

    app.logger.debug(f"Babel default locale: {app.config['BABEL_DEFAULT_LOCALE']}")
    app.logger.debug(f"Babel supported locales: {app.config['BABEL_SUPPORTED_LOCALES']}")
    app.logger.debug(f"Babel translation directories: {app.config['BABEL_TRANSLATION_DIRECTORIES']}")

    cors.init_app(app, resources={r"/*": {"origins": os.getenv('FRONTEND_URL'), "allow_headers": ["Content-Type", "Authorization"], "supports_credentials": True}})

    db.init_app(app)
    mail_instance.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)

    def get_locale():
        best_match = request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])
        app.logger.debug(f"Best matched locale: {best_match}")
        return best_match

    babel.locale_selector_func = get_locale

    from routes.auth import auth_bp
    from routes.session import session_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(session_bp, url_prefix='/session')

    @app.route('/test_translation')
    def test_translation():
        preferred_language = 'fr'
        with force_locale(preferred_language):
            translated_text = gettext('Reset Your Password')
            app.logger.debug(f"Translated text: {translated_text}")
            return translated_text

    @app.route('/test_manual_translation')
    def test_manual_translation():
        from babel.support import Translations

        preferred_language = 'fr'
        translation_dir = os.path.join(os.path.dirname(__file__), '..', os.getenv('BABEL_TRANSLATION_DIRECTORIES'))
        translations = Translations.load(translation_dir, [preferred_language])
        translated_text = translations.gettext('Reset Your Password')

        app.logger.debug(f"Manually translated text: {translated_text}")
        return translated_text

    return app
