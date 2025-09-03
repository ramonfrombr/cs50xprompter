from app import create_app, socketio
from database import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # or handle via flask db upgrade in entrypoint
    socketio.run(app, host="0.0.0.0", port=5000)
