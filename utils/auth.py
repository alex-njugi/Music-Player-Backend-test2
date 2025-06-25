from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from functools import wraps
# from models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(password, password_hash):
    return bcrypt.check_password_hash(password_hash, password)

def create_access_token(user_id):
    return create_access_token(identity=user_id)

def verify_token(token):
    try:
        verify_jwt_in_request(token)
        return get_jwt_identity()
    except:
        return None

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except:
            return jsonify({"error": "Unauthorized"}), 401
    return wrapper