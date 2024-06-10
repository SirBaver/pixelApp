from celery import Celery
from datetime import datetime, timezone
from models import db, UserIdle
from backend.app2 import app, celery, redis_client  # Import app, celery, and redis_client from app.py

@celery.task
def batch_update_connections():
    keys = redis_client.keys('user:*:last_connection')
    for key in keys:
        user_id = key.split(b':')[1].decode('utf-8')
        last_connection = datetime.fromisoformat(redis_client.get(key).decode('utf-8'))
        user_idle = UserIdle.query.filter_by(user_id=user_id).first()
        if user_idle:
            user_idle.last_connection = last_connection
            db.session.commit()

# Schedule the task to run every hour
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'batch-update-connections-every-hour': {
        'task': 'tasks.batch_update_connections',
        'schedule': crontab(minute=0, hour='*'),
    },
}
