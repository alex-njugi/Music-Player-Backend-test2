from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from routes.song_routes import song_bp


app = Flask(__name__)

db = SQLAlchemy(app)
jwt = JWTManager(app)

app.register_blueprint(song_bp)

from models import Song, User

if __name__ == '__main__':
    app.run(debug=True)