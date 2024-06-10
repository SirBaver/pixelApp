from flask import Flask, request, session, jsonify
from flask_cors import CORS
from redis import Redis
from werkzeug.security import generate_password_hash, check_password_hash
from database import db  # import db from database.py
from models import User, UserIdle
from celery import Celery
import os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # IMPORTANT : Configuration prod à changer
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1234ABCD!' # UNIQUEMENT POUR TEST LOCAL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Gain ratios
app.config['BASE_GAIN'] = 1.0
app.config['PREMIUM_MULTIPLIER'] = 2.0

# Configuration de MailHog
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
db.init_app(app)

# Configurez Flask-Mail ici
mail_instance = Mail(app)

# Générateur de token sécurisé
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Redis configuration
redis_client = Redis(host='localhost', port=6379, db=0)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@app.route('/')
def index():
    return "Hello, World!"

import re

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    mail = data.get('mail')

    # Validation de l'email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, mail):
        return jsonify({'message': 'Invalid email format'}), 400
    
    if username and password and mail:
        user_by_username = User.query.filter_by(username=username).first()
        user_by_mail = User.query.filter_by(mail=mail).first()
        
        if user_by_username:
            return jsonify({'message': 'Username already exists'}), 409
        if user_by_mail:
            return jsonify({'message': 'Email already exists'}), 409

        password_hash = generate_password_hash(password)
        verification_token = s.dumps(mail, salt='email-confirm')
        
        try:
            user = User(username=username, _password=password_hash, mail=mail, verification_token=verification_token, is_verified=False)
            db.session.add(user)
            db.session.commit()
            print(f"User {username} created successfully.")
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': 'Database error'}), 500
        
        # Envoyer l'email de vérification
        verification_url = f"http://localhost:5000/verify_email?token={verification_token}"
        msg = Message('Confirmez votre adresse email', sender='noreply@example.com', recipients=[mail])
        msg.body = f'Pour confirmer votre adresse email, veuillez cliquer sur le lien suivant: {verification_url}'
        
        try:
            mail_instance.send(msg)
            print(f"Verification email sent to {mail}.")
        except Exception as e:
            print(f"Error sending email: {e}")

        return jsonify({'message': 'Success. Please check your email to confirm your registration.'}), 200
    else:
        print("Missing username, password, or mail.")
        return jsonify({'message': 'Missing username, password, or mail'}), 422

@app.route('/resend_verification', methods=['POST'])
def resend_verification():
    data = request.get_json()
    mail = data.get('mail')

    # Validation de l'email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, mail):
        return jsonify({'message': 'Invalid email format'}), 400

    user = User.query.filter_by(mail=mail).first()
    if user:
        if user.is_verified:
            return jsonify({'message': 'This account is already verified.'}), 400

        # Générer un nouveau token de vérification
        verification_token = s.dumps(mail, salt='email-confirm')
        user.verification_token = verification_token
        db.session.commit()
        
        # Envoyer l'email de vérification
        verification_url = f"http://localhost:5000/verify_email?token={verification_token}"
        msg = Message('Confirmez votre adresse email', sender='noreply@example.com', recipients=[mail])
        msg.body = f'Pour confirmer votre adresse email, veuillez cliquer sur le lien suivant: {verification_url}'
        
        try:
            mail_instance.send(msg)
            print(f"Verification email resent to {mail}.")
            return jsonify({'message': 'Verification email has been resent. Please check your email.'}), 200
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({'message': 'Error sending email.'}), 500
    else:
        return jsonify({'message': 'Email not found'}), 404


@app.route('/verify_email', methods=['GET'])
def verify_email():
    token = request.args.get('token')
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)  # Token valide pour 1 heure
    except (SignatureExpired, BadSignature):
        return jsonify({'message': 'The token is invalid or has expired.'}), 400

    user = User.query.filter_by(mail=email).first()
    if user and not user.is_verified:
        user.is_verified = True
        db.session.commit()
        return jsonify({'message': 'Your account has been verified successfully.'}), 200
    else:
        return jsonify({'message': 'This account is already verified or does not exist.'}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user._password, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return 'Invalid username or password', 401  # Unauthorized

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
