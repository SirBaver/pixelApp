from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_babel import Babel
from flask_cors import CORS
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer

db = SQLAlchemy()
mail_instance = Mail()
babel = Babel()
cors = CORS()
migrate = Migrate()
s = URLSafeTimedSerializer('1234ABCD!')

def init_app(app):
    db.init_app(app)
    mail_instance.init_app(app)
    babel.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
