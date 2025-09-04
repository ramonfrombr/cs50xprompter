import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from .config import Config, TestingConfig
from .events import register_events

db = SQLAlchemy()
# Create global instances so extensions can be used in blueprints
socketio = SocketIO(async_mode='eventlet', cors_allowed_origins='*')
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)

    if config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    # Register event handlers
    register_events(socketio)

    return app
