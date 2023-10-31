from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
bcrypt = Bcrypt(app)

# User class for authentication
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
        db.commit()
        cursor.close()
        db.close()

def authenticate(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    if user and bcrypt.check_password_hash(user['password'], password):
        return User(user['id'], user['username'], user['password'])

def identity(payload):
    user_id = payload['identity']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    if user:
        return User(user['id'], user['username'], user['password'])

jwt = JWTManager(app)

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')

    db = get_db()
    cursor = db.cursor()
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({'message': 'Signup successful'})

@app.route('/ping')
def ping():
    return 'Ping successful!'

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = authenticate(username, password)
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})

    return jsonify({'message': 'Invalid username or password'}), 401

# Protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({'message': f'Hello, user {current_user_id}! This is a protected endpoint.'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
