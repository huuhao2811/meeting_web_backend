from .users import users_bp
from .meetings import meetings_bp
from .messages import messages_bp
from .meeting_participants import participants_bp
from .recordings import recordings_bp

def register_blueprints(app):
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(meetings_bp, url_prefix="/api/meetings")
    app.register_blueprint(messages_bp, url_prefix="/api/messages")
    app.register_blueprint(participants_bp, url_prefix="/api/participants")
    app.register_blueprint(recordings_bp, url_prefix="/api/recordings")
