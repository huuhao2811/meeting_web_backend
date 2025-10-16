from flask import Flask
from flask_mail import Mail
from config import Config
from extensions import db, migrate, jwt, cors, mail, socketio
from routes import register_blueprints
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    register_blueprints(app)


    return app


if __name__ == "__main__":
    app = create_app()
    from sockets.socket_events import * 
    from sockets.chat_events import *
    from sockets.micro_events import *
    from sockets.camera_events import *
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
