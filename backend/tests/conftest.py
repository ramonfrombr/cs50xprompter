import pytest
from sqlalchemy.orm import sessionmaker, scoped_session
from app import create_app, db


@pytest.fixture(scope="session")
def app():
    # Use testing config (make sure you have TESTING=True and sqlite memory DB)
    app = create_app("testing")
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def _db(app):
    # Create all tables once per test session
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture(autouse=True)
def session(_db):
    connection = _db.engine.connect()
    transaction = connection.begin()

    SessionFactory = sessionmaker(bind=connection)
    session = scoped_session(SessionFactory)

    _db.session = session

    yield session

    session.remove()
    transaction.rollback()
    connection.close()
