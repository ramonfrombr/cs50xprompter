from flask import request


def register_events(socketio):
    @socketio.on("connect")
    def handle_connect():
        print("A user connected:", request.sid)
