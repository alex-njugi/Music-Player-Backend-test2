from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)