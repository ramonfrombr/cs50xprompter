from app import create_app, socketio
from app.database import db

app = create_app()

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    socketio.run(app, host="0.0.0.0", port=5000)
