from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

from models.db import db
from config import Config
from routes.auth_routes import auth_bp
from routes.song_routes import song_bp
from models.user import User  # make sure all models are imported
from models.song import Song

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(song_bp)

@app.route("/")
def index():
    return {"message": "Music Player Backend is live"}

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created.")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
