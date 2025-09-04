import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from functools import wraps
from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request
from database import db
from models import User


auth = Blueprint("auth", __name__)

SECRET_KEY = "secret"


@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    exp = datetime.now(timezone.utc) + timedelta(hours=12)
    payload = {"user_id": user.id, "exp": int(exp.timestamp())}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["user_id"])
        except ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except InvalidTokenError:
            return jsonify({"error": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@auth.route("/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    return jsonify({"message": f"Hello {current_user.username}, you are authenticated!"})
