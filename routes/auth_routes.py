print("auth_routes.py loaded")

from flask import Blueprint
from controllers.auth_controller import register_user, login_user, get_profile

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

auth_bp.route("/register", methods=["POST"])(register_user)
auth_bp.route("/login", methods=["POST"])(login_user)
auth_bp.route("/profile", methods=["GET"])(get_profile)
