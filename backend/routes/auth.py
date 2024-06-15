from flask import Blueprint, request, jsonify, session, current_app, url_for, redirect
from flask_babel import lazy_gettext as _l, gettext, force_locale
from flask_mail import Message
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import re
import logging
import os
import uuid

from extensions import db, mail_instance, s
from models import User, Session

auth_bp = Blueprint('auth', __name__)

# Configurer le logger
logging.basicConfig(level=logging.DEBUG)

@auth_bp.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', os.getenv('FRONTEND_URL'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@auth_bp.route('/register', methods=['POST'])
@cross_origin(origins=os.getenv('FRONTEND_URL'))
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
            # Commencez une transaction
            user = User(username=username, _password=password_hash, mail=mail, verification_token=verification_token, is_verified=False, preferred_language=preferred_language)
            db.session.add(user)
            db.session.flush()  # Assurez-vous que l'ID de l'utilisateur est disponible

            # Créer une session et y stocker l'adresse e-mail
            session_id = uuid.uuid4()
            expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            new_session = Session(id=session_id, user_id=user.id, data={'mail': mail}, expires_at=expires_at)
            db.session.add(new_session)

            # Commit une fois toutes les opérations réussies
            db.session.commit()
            logging.debug(f"User {username} created successfully.")

        except Exception as e:
            db.session.rollback()
            logging.error(f"Database error: {e}")
            return jsonify({'message': f'Database error: {e}'}), 500

        # Envoyer l'email de vérification
        verification_url = url_for('auth.verify_email', token=verification_token, _external=True)

        with force_locale(preferred_language):
            logging.debug(f"Sending email in language: {preferred_language}")
            msg = Message(gettext('Confirm your email'), sender='noreply@example.com', recipients=[mail])
            msg.body = gettext('To confirm your email, please click on the following link: %(url)s', url=verification_url)

        try:
            mail_instance.send(msg)
            logging.debug(f"Verification email sent to {mail}.")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

        return jsonify({'message': 'Success. Please check your email to confirm your registration.', 'session_id': str(session_id)}), 200
    else:
        logging.error("Missing username, password, or mail.")
        return jsonify({'message': 'Missing username, password, or mail'}), 422

@auth_bp.route('/resend_verification', methods=['POST'])
@cross_origin(origins=os.getenv('FRONTEND_URL'))
def resend_verification():
    data = request.get_json()
    session_id_str = data.get('session_id')

    try:
        session_id = uuid.UUID(session_id_str)  # Convertir en UUID
    except ValueError:
        logging.error(f"Invalid session ID format: {session_id_str}")
        return jsonify({'message': 'Invalid session ID format'}), 400

    session_obj = Session.query.get(session_id)
    if not session_obj:
        logging.error("Session not found")
        return jsonify({'message': 'Session not found'}), 400
    
    # Convertir l'expiration de la session en offset-aware datetime si ce n'est pas le cas
    if session_obj.expires_at.tzinfo is None:
        session_obj.expires_at = session_obj.expires_at.replace(tzinfo=timezone.utc)
    
    current_time = datetime.now(timezone.utc)
    if session_obj.expires_at < current_time:
        logging.error("Session expired")
        return jsonify({'message': 'Session expired'}), 400

    mail = session_obj.data.get('mail')

    # Validation de l'email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, mail):
        logging.error("Invalid email format")
        return jsonify({'message': 'Invalid email format'}), 400

    user = User.query.filter_by(mail=mail).first()
    if user:
        if user.is_verified:
            logging.error("This account is already verified.")
            return jsonify({'message': 'This account is already verified.'}), 400

        # Récupérer la langue préférée de l'utilisateur
        preferred_language = user.preferred_language

        # Générer un nouveau token de vérification
        verification_token = s.dumps(mail, salt='email-confirm')
        user.verification_token = verification_token
        db.session.commit()

        # Envoyer l'email de vérification
        verification_url = url_for('auth.verify_email', token=verification_token, _external=True)

        with force_locale(preferred_language):
            msg = Message(gettext('Confirm your email'), sender='noreply@example.com', recipients=[mail])
            msg.body = gettext('To confirm your email, please click on the following link: %(url)s', url=verification_url)

        try:
            mail_instance.send(msg)
            logging.debug(f"Verification email resent to {mail}.")
            return jsonify({'message': 'Verification email has been resent. Please check your email.'}), 200
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return jsonify({'message': 'Error sending email.'}), 500
    else:
        logging.error("Email not found")
        return jsonify({'message': 'Email not found'}), 404

@auth_bp.route('/resend_reset', methods=['POST'])
@cross_origin(origins=os.getenv('FRONTEND_URL'))
def resend_reset():
    data = request.get_json()
    session_id_str = data.get('session_id')  # session_id from the frontend

    try:
        # Convert session_id to UUID
        session_id = uuid.UUID(session_id_str)
    except ValueError:
        logging.error(f"Invalid session ID format: {session_id_str}")
        return jsonify({'message': 'Invalid session ID format'}), 400

    session_obj = Session.query.get(session_id)
    if not session_obj:
        logging.error("Session not found")
        return jsonify({'message': 'Session not found'}), 400

    if session_obj.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):  # Convert expires_at to aware
        logging.error("Session expired")
        return jsonify({'message': 'Session expired'}), 400

    mail = session_obj.data.get('mail')

    # Validation de l'email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, mail):
        logging.error("Invalid email format")
        return jsonify({'message': 'Invalid email format'}), 400

    user = User.query.filter_by(mail=mail).first()
    if user:
        # Récupérer la langue préférée de l'utilisateur
        preferred_language = user.preferred_language

        # Générer un nouveau token de réinitialisation
        reset_token = s.dumps(mail, salt='password-reset')
        user.reset_token = reset_token
        user.reset_token_expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        db.session.commit()

        # Envoyer l'email de réinitialisation
        reset_url = f"{os.getenv('API_URL')}/auth/password_reset?token={reset_token}"

        with force_locale(preferred_language):
            msg = Message(gettext('Reset Your Password'), sender='noreply@example.com', recipients=[mail])
            msg.body = gettext('To reset your password, click the following link: %(url)s', url=reset_url)

        try:
            mail_instance.send(msg)
            logging.debug(f"Password reset email resent to {mail}.")
            return jsonify({'message': 'Password reset email has been resent. Please check your email.'}), 200
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return jsonify({'message': 'Error sending email.'}), 500
    else:
        logging.error("Email not found")
        return jsonify({'message': 'Email not found'}), 404

@auth_bp.route('/verify_email', methods=['GET'])
@cross_origin(origins=os.getenv('FRONTEND_URL'))
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
        return redirect(f"{os.getenv('FRONTEND_URL')}/home")  # Rediriger vers la page d'accueil
    else:
        return jsonify({'message': 'This account is already verified or does not exist.'}), 400

@auth_bp.route('/login', methods=['POST'])
@cross_origin(origins=os.getenv('FRONTEND_URL'))
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
@cross_origin(origins=os.getenv('FRONTEND_URL'))
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
        user.reset_token_expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        db.session.commit()
        
        # Créer une session pour stocker l'adresse email
        session_id = uuid.uuid4()  # Générer un UUID
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        new_session = Session(id=session_id, user_id=user.id, data={'mail': mail}, expires_at=expires_at)
        db.session.add(new_session)
        db.session.commit()

        # Envoyer l'email de réinitialisation
        reset_url = f"{os.getenv('API_URL')}/auth/password_reset?token={reset_token}"
        with force_locale(user.preferred_language):
            msg = Message(gettext('Reset Your Password'), sender='noreply@example.com', recipients=[mail])
            msg.body = gettext('To reset your password, click the following link: %(url)s', url=reset_url)
        
        try:
            mail_instance.send(msg)
            logging.debug(f"Password reset email sent to {mail}.")
            return jsonify({'message': gettext('Password reset email has been sent. Please check your email.'), 'session_id': str(session_id)}), 200
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return jsonify({'message': gettext('Error sending email.')}), 500
    else:
        return jsonify({'message': gettext('Email not found')}), 404

@auth_bp.route('/password_reset', methods=['GET'])
@cross_origin(origins=os.getenv('FRONTEND_URL'))
def reset_password_page():
    token = request.args.get('token')
    if not token:
        return jsonify({'message': 'Token is missing'}), 400
    
    try:
        mail = s.loads(token, salt='password-reset', max_age=3600)
    except (SignatureExpired, BadSignature):
        return jsonify({'message': 'The token is invalid or has expired.'}), 400

    # Redirigez l'utilisateur vers l'application frontend avec le token
    return redirect(f"{os.getenv('FRONTEND_URL')}/password-reset?token={token}")

@auth_bp.route('/reset_password', methods=['POST'])
@cross_origin(origins=os.getenv('FRONTEND_URL'))
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')
    
    try:
        mail = s.loads(token, salt='password-reset', max_age=3600)
    except (SignatureExpired, BadSignature):
        return jsonify({'message': gettext('The token is invalid or has expired.')}), 400

    user = User.query.filter_by(mail=mail).first()
    if user and user.reset_token == token and user.reset_token_expiration > datetime.now(timezone.utc):
        user.password = new_password  # Utilisez le setter pour hacher le mot de passe
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()
        return jsonify({'message': gettext('Your password has been reset successfully.')}), 200
    else:
        return jsonify({'message': gettext('Invalid token or the token has expired.')}), 400

@auth_bp.route('/logout')
@cross_origin(origins=os.getenv('FRONTEND_URL'))
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200
