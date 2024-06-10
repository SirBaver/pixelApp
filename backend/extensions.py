from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_babel import Babel
from itsdangerous import URLSafeTimedSerializer

db = SQLAlchemy()
mail_instance = Mail()
babel = Babel()
s = URLSafeTimedSerializer('1234ABCD!')
