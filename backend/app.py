import bcrypt
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config
from database import db
from events import register_events

# Create global instances so extensions can be used in blueprints
socketio = SocketIO(async_mode='eventlet', cors_allowed_origins='*')
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from models import User, ScriptGroup, Script

    from auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    # Register event handlers
    register_events(socketio)

    return app
