from flask import request
from flask_socketio import SocketIO, emit


def register_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        # Use `request.sid` only via flask_socketio `request` context
        print("A user connected:", request.sid)
        emit("message", {"data": f"Welcome {request.sid}"})

    @socketio.on("disconnect")
    def handle_disconnect():
        print("A user disconnected:", request.sid)
