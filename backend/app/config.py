import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # ✅ fast, isolated
    SQLALCHEMY_TRACK_MODIFICATIONS = False
