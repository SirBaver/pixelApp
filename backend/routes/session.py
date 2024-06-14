from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import uuid
from extensions import db
from models import User, Session
import os

session_bp = Blueprint('session', __name__)

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

    # Générer un ID de session unique
    session_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)  # Durée de vie de la session : 1 heure

    new_session = Session(id=session_id, user_id=user_id, data=session_data, expires_at=expires_at)
    db.session.add(new_session)
    db.session.commit()

    return jsonify({'message': 'Session created', 'session_id': session_id}), 201

@session_bp.route('/get_session/<session_id>', methods=['GET'])
def get_session(session_id):
    session = Session.query.get(session_id)
    if session and session.expires_at > datetime.now(timezone.utc) + timedelta(hours=1):
        return jsonify({'session_data': session.data})
    return jsonify({'message': 'Session not found or expired'}), 404

@session_bp.route('/delete_session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get(session_id)
    if session:
        db.session.delete(session)
        db.session.commit()
        return jsonify({'message': 'Session deleted'}), 200
    return jsonify({'message': 'Session not found'}), 404
