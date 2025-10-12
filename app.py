from flask import Flask
from flask_mail import Mail
from config import Config
from extensions import db, migrate, jwt, cors, mail
from routes import register_blueprints
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register blueprints
    register_blueprints(app)

    @app.route("/api/health")
    def health_check():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5001)
