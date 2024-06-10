from datetime import datetime, timezone, timedelta
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

# 1 - Table User
class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    google_id = db.Column(db.String(120), unique=True, nullable=True)
    apple_id = db.Column(db.String(120), unique=True, nullable=True)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True)
    provider = db.Column(db.String(120), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(120), nullable=True)
    reset_token = db.Column(db.String(120), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)
    is_premium = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    pixel_stock = db.Column(db.Integer, default=0)
    preferred_language = db.Column(db.String(5), default='en')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

# 2 - Table UserPixels -- Depreciated
# class UserPixels(db.Model):
#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False, unique=True)
#     pixels_account = db.Column(db.Integer, nullable=False, default=0)

# 3 - Table UserIdle
class UserIdle(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    last_connection = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    gain_ratio = db.Column(db.Float, default=0.0)

    def is_idle_expired(self):
        return (datetime.now(timezone.utc) - self.last_connection) > timedelta(hours=48)

    def update_last_connection(self):
        self.last_connection = datetime.now(timezone.utc)
        redis_client.set(f"user:{self.user_id}:last_connection", self.last_connection.isoformat())
        db.session.commit()

    def calculate_gain(self):
        user = User.query.get(self.user_id)
        if self.is_idle_expired():
            return 0
        base_gain = self.gain_ratio * app.config['BASE_GAIN']
        if user.is_premium:
            base_gain *= app.config['PREMIUM_MULTIPLIER']
        return base_gain

# 4 - Table UserAds
class UserAds(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    ads_watched = db.Column(db.Integer, nullable=False, default=0)
    last_ad_watch = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def can_watch_ad(self):
        # Check if user has watched 3 ads in the last 24 hours
        return self.ads_watched < 3 and (datetime.now(timezone.utc) - self.last_ad_watch) > timedelta(hours=24)

    def watch_ad(self):
        self.ads_watched += 1
        self.last_ad_watch = datetime.now(timezone.utc)
        db.session.commit()
        return self.ads_watched

# 5 - Table UserPurchases
class UserPurchases(db.Model):
    purchase_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    expiration_date = db.Column(db.DateTime, nullable=True)

    def is_premium(self):
        return self.expiration_date and self.expiration_date > datetime.now(timezone.utc)

    def purchase_premium(self, product_id, expiration_date):
        self.product_id = product_id
        self.expiration_date = expiration_date
        db.session.commit()
        return self.expiration_date

# 6 - Table Product
class Product(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)