from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
import uuid
from extensions import db
from models import User, Session
import logging
import os

session_bp = Blueprint('session', __name__)

# Configurer le logger
logging.basicConfig(level=logging.DEBUG)

@session_bp.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', os.getenv('FRONTEND_URL'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@session_bp.route('/create_session', methods=['POST'])
def create_session():
    data = request.get_json()
    user_id = data.get('user_id')
    session_data = data.get('data', {})

    if not user_id:
        logging.error("Missing user_id in request data.")
        return jsonify({'message': 'Missing user_id'}), 400

    # Vérifiez si l'utilisateur existe
    user = User.query.get(user_id)
    if not user:
        logging.error(f"User with id {user_id} not found.")
        return jsonify({'message': 'User not found'}), 404

    # Générer un ID de session unique
    session_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)  # Durée de vie de la session : 1 heure

    try:
        new_session = Session(id=session_id, user_id=user_id, data=session_data, expires_at=expires_at)
        db.session.add(new_session)
        db.session.commit()
        logging.debug(f"Session {session_id} created for user {user_id}.")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error: {e}")
        return jsonify({'message': 'Database error'}), 500

    return jsonify({'message': 'Session created', 'session_id': session_id}), 201

@session_bp.route('/get_session/<session_id>', methods=['GET'])
def get_session(session_id):
    try:
        session_id = uuid.UUID(session_id)  # Convertir en UUID
    except ValueError:
        logging.error(f"Invalid session ID format: {session_id}")
        return jsonify({'message': 'Invalid session ID format'}), 400

    session = Session.query.get(session_id)
    if session:
        if session.expires_at.tzinfo is None:
            session.expires_at = session.expires_at.replace(tzinfo=timezone.utc)

        if session.expires_at > datetime.now(timezone.utc):
            logging.debug(f"Session {session_id} retrieved.")
            return jsonify({'session_data': session.data})
        else:
            logging.error(f"Session {session_id} has expired.")
            return jsonify({'message': 'Session expired'}), 404
    else:
        logging.error(f"Session {session_id} not found.")
        return jsonify({'message': 'Session not found'}), 404

@session_bp.route('/delete_session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        session_id = uuid.UUID(session_id)  # Convertir en UUID
    except ValueError:
        logging.error(f"Invalid session ID format: {session_id}")
        return jsonify({'message': 'Invalid session ID format'}), 400

    session = Session.query.get(session_id)
    if session:
        try:
            db.session.delete(session)
            db.session.commit()
            logging.debug(f"Session {session_id} deleted.")
            return jsonify({'message': 'Session deleted'}), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Database error: {e}")
            return jsonify({'message': 'Database error'}), 500
    else:
        logging.error(f"Session {session_id} not found.")
        return jsonify({'message': 'Session not found'}), 404
