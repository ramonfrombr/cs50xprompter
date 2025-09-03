from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from config import Config
from database import db
from events import register_events

# Create global instances so extensions can be used in blueprints
socketio = SocketIO(async_mode='eventlet', cors_allowed_origins='*')
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # 👇 ensure models are registered
    from models import User, ScriptGroup, Script

    # Register event handlers
    register_events(socketio)

    return app
