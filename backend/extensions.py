from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_babel import Babel
from itsdangerous import URLSafeTimedSerializer
from flask_cors import CORS  # Importer flask-cors

db = SQLAlchemy()
mail_instance = Mail()
babel = Babel()
s = URLSafeTimedSerializer('1234ABCD!')
cors = CORS()  # Initialiser CORS
