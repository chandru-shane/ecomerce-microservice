import json
import pytest
import pytest_mock
from app import create_app, db
from flask_jwt_extended import create_access_token
from app.models import User




@pytest.fixture
def client():
    app = create_app(testing=True)
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user():
    user = User(username="testuser01", password="testuser01")
    db.session.add(user)
    db.session.commit()
    return user



def test_login_view(client):
    payload = {
        "username":"testuser01",
        "password":"testuser01"
    }
    response = client.post("/api/user", json=payload, headers={'Content-Type': 'application/json'})

    response = client.post("/api/login", json=payload)
    print(response.data)
    assert response.status_code == 200
    assert response.json.get("access_token") and response.json.get("refresh_token")



def test_me_view(client, user):
    data = {
        "username":"testuser01",
        "password":"testuser01"
    }
    user = User.query.filter(User.username==data.get("username")).first()
    access_token = create_access_token(identity=data.get("username"))
    
    response = client.get("/api/me", json=data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json.get("username") == data.get("username")



def test_update_password_view(client, user):
    data = {
        "password":"newpass123"
    }

    access_token = create_access_token(identity=user.as_dict().get("username"))
    
    response = client.put("/api/user_update", data=data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    data["username"] = user.as_dict().get("username")
    response = client.post("/api/login", json=data)
    print(response.json)
    assert response.status_code == 200
    access_token = response.json.get("access_token")
    response = client.get("/api/me", json=data, headers={"Authorization": f"Bearer {access_token}"})
    print(response.json)
    
    assert response.status_code == 200
