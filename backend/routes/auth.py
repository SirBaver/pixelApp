from flask import Blueprint, request, jsonify, session
from extensions import db, mail_instance, s
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import gettext
from datetime import datetime, timedelta
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    mail = data.get('mail')
    preferred_language = data.get('preferred_language', 'en')

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
            user = User(username=username, _password=password_hash, mail=mail, verification_token=verification_token, is_verified=False, preferred_language=preferred_language)
            db.session.add(user)
            db.session.commit()
            print(f"User {username} created successfully.")
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': 'Database error'}), 500

        # Envoyer l'email de vérification
        verification_url = f"http://localhost:5000/auth/verify_email?token={verification_token}"
        
        # Utiliser la langue préférée pour l'email
        msg = Message(gettext('Confirm your email', locale=preferred_language), sender='noreply@example.com', recipients=[mail])
        msg.body = gettext('To confirm your email, please click on the following link: %(url)s', url=verification_url, locale=preferred_language)

        try:
            mail_instance.send(msg)
            print(f"Verification email sent to {mail}.")
        except Exception as e:
            print(f"Error sending email: {e}")

        return jsonify({'message': 'Success. Please check your email to confirm your registration.'}), 200
    else:
        print("Missing username, password, or mail.")
        return jsonify({'message': 'Missing username, password, or mail'}), 422


@auth_bp.route('/resend_verification', methods=['POST'])
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
        verification_url = f"http://localhost:5000/auth/verify_email?token={verification_token}"
        msg = Message(gettext('Confirm your email'), sender='noreply@example.com', recipients=[mail])
        msg.body = gettext('To confirm your email, please click on the following link: %(url)s', url=verification_url)
        
        try:
            mail_instance.send(msg)
            print(f"Verification email resent to {mail}.")
            return jsonify({'message': 'Verification email has been resent. Please check your email.'}), 200
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({'message': 'Error sending email.'}), 500
    else:
        return jsonify({'message': 'Email not found'}), 404

@auth_bp.route('/verify_email', methods=['GET'])
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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mail = data.get('mail')
    password = data.get('password')
    
    # Validation de l'email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, mail):
        return jsonify({'message': 'Invalid email format'}), 400
    
    user = User.query.filter_by(mail=mail).first()
    
    if user and check_password_hash(user._password, password):
        if not user.is_verified:
            return jsonify({'message': 'Account not verified. Please check your email to verify your account.'}), 403
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401  # Unauthorized

@auth_bp.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    mail = data.get('mail')
    
    # Validation de l'email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, mail):
        return jsonify({'message': 'Invalid email format'}), 400
    
    user = User.query.filter_by(mail=mail).first()
    if user:
        # Générer un token de réinitialisation
        reset_token = s.dumps(mail, salt='password-reset')
        user.reset_token = reset_token
        user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        
        # Envoyer l'email de réinitialisation
        reset_url = f"http://localhost:5000/auth/reset_password?token={reset_token}"
        msg = Message(gettext('Reset Your Password'), sender='noreply@example.com', recipients=[mail])
        msg.body = gettext('To reset your password, click the following link: %(url)s', url=reset_url)
        
        try:
            mail_instance.send(msg)
            print(f"Password reset email sent to {mail}.")
            return jsonify({'message': 'Password reset email has been sent. Please check your email.'}), 200
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({'message': 'Error sending email.'}), 500
    else:
        return jsonify({'message': 'Email not found'}), 404

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    try:
        mail = s.loads(token, salt='password-reset', max_age=3600)
    except (SignatureExpired, BadSignature):
        return jsonify({'message': 'The token is invalid or has expired.'}), 400

    user = User.query.filter_by(mail=mail).first()
    if user and user.reset_token == token and user.reset_token_expiration > datetime.utcnow():
        user._password = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()
        return jsonify({'message': 'Your password has been reset successfully.'}), 200
    else:
        return jsonify({'message': 'Invalid token or the token has expired.'}), 400

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200
