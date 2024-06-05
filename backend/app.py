from flask import Flask, request, session, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from database import db  # import db from database.py
from models import User, Pixel

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # IMPORTANT : Configuration prod à changer
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1234ABCD!' # UNIQUEMENT POUR TEST LOCAL
db.init_app(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # for debugging
    print(f'username: {username}, password: {password}')
    if username and password:
        # Check if username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return 'Username already exists', 409
        password = generate_password_hash(password)
        try:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            return 'Database error', 500
        return jsonify({'message': 'Success'}), 200
    else:
        return 'Missing username or password', 422

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user._password, password):  # use user._password instead of user.password
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return 'Invalid username or password'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)