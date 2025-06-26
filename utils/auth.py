from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

def create_access_token_for_user(user_id):
    return create_access_token(identity=user_id)
