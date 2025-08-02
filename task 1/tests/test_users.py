import pytest
from app import app, db
from models.user import User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
        yield client

def test_health(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["status"] == "OK"
