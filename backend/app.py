from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database import db  # import db from database.py
from models import User, Pixel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1234ABCD!'
db.init_app(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

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