import json
import pytest
import pytest_mock
from app import create_app, db
from app.models import Order
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


@pytest.fixture
def mock_requests_get(mocker):
    def mock_get(url, headers):
        if headers.get('Authorization') == 'Bearer valid_token':
            return mocker.Mock(status_code=200, json=lambda: {'id': 1, 'username': 'test_user'})
        else:
            return mocker.Mock(status_code=401)

    return mocker.patch('app.auth.requests.get', side_effect=mock_get)

@pytest.fixture
def mock_product_requests_get(mocker, mock_requests_get):
    def mock_get_product(request, product_id):
        return {"id":1, "user_id":1, "product_id":1, "price":"10.00"}

    return mocker.patch("app.resources.get_product", side_effect=mock_get_product)

@pytest.fixture
def client():
    app = create_app(testing=True)
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()


def test_order_list_with_auth(client, mock_requests_get):
    order1 = Order(user_id=1, product_id=1, quantity=1, price=10.00)
    order2 = Order(user_id=1, product_id=2, quantity=1, price=10.00)
    order3 = Order(user_id=2, product_id=2, quantity=1, price=10.00)
    db.session.add_all([order1, order2, order3])
    db.session.commit()

    response = client.get('/api/orders', headers={'Authorization': 'Bearer valid_token'})

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert len(response.json) == 2


def test_order_list_without_auth(client, mock_requests_get):
    order1 = Order(user_id=1, product_id=1, quantity=1, price=10.00)
    order2 = Order(user_id=1, product_id=2, quantity=1, price=10.00)
    order3 = Order(user_id=2, product_id=2, quantity=1, price=10.00)
    db.session.add_all([order1, order2, order3])
    db.session.commit()

    response = client.get('/api/orders', headers={'Authorization': 'Bearer invalid_token'})

    # Assert that the response status code is 200
    assert response.status_code == 401

def test_order_post_with_auth(client, mock_requests_get, mock_product_requests_get):
    data = {
        "user_id": 1,
        "product_id": 1,
        "price": "10.00",
        "quantity": 10
    }
    response = client.post('/api/orders', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'}, json=data)
    assert response.status_code == 201
    assert len(Order.query.all()) == 1


def test_order_post_without_auth(client, mock_requests_get):
    data = {
        "user_id":1,
        "product_id":1,
        "price":"10.00",
        "quantity":10
    }
    response = client.post('/api/orders', headers={'Authorization': 'Bearer invalid_token', 'Content-Type': 'application/json'}, data=json.dumps(data))
    # Assert that the response status code is 200
    assert response.status_code == 401


def test_order_retrive_without_auth(client, mock_requests_get):
    order1 = Order(user_id=1, product_id=1, quantity=1, price=10.00)
    order3 = Order(user_id=2, product_id=2, quantity=1, price=10.00)
    db.session.add_all([order1, order3])
    db.session.commit()

    response = client.get('/api/orders/1', headers={'Authorization': 'Bearer invalid_token', 'Content-Type': 'application/json'})

    # Assert that the response status code is 200
    assert response.status_code == 401
    data = order1.as_dict()
    data["status"] = "on_the_way"
    response = client.put(f'/api/orders/{order1.id}', headers={'Authorization': 'Bearer invalid_token', 'Content-Type': 'application/json'}, data=json.dumps(data, cls=CustomJSONEncoder))
    assert  response.status_code == 401
    updated_order = Order.query.filter(Order.id==order1.id).first()
    assert  order1.as_dict() == updated_order.as_dict()
    response = client.delete(f'/api/orders/{order1.id}', headers={'Authorization': 'Bearer invalid_token', 'Content-Type': 'application/json'})
    assert response.status_code == 401
    assert  Order.query.filter(Order.id==order1.id).first()


def test_order_retrive_with_auth(client, mock_requests_get):
    order1 = Order(user_id=1, product_id=1, quantity=1, price=10.00)
    order2 = Order(user_id=2, product_id=2, quantity=1, price=10.00)
    db.session.add_all([order1, order2])
    db.session.commit()
    
    response = client.get(f'/api/orders/{order1.id}', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'})
    assert response.status_code == 200
    data = order1.as_dict()
    data["status"] = "on_the_way"
    
    response = client.put(f'/api/orders/{order1.id}', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'}, data=json.dumps(data, cls=CustomJSONEncoder))
    assert  response.status_code == 200
    updated_order = Order.query.filter(Order.id==order1.id).first()
    # assert  order1.as_dict() != updated_order.as_dict()
    assert  data["status"] == updated_order.as_dict()["status"]
    
    response = client.delete(f'/api/orders/{order1.id}', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'})
    assert response.status_code == 204
    assert  Order.query.filter(Order.id==order1.id).first() is None

    response = client.get(f'/api/orders/{order2.id}', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'})
    assert response.status_code == 403
    data = order2.as_dict()
    data["status"] = "on_the_way"
    
    response = client.put(f'/api/orders/{order1.id}', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'}, data=json.dumps(data, cls=CustomJSONEncoder))
    updated_order = Order.query.filter(Order.id==order2.id).first()
    assert response.status_code == 403
    assert  data["status"] != updated_order.as_dict()["status"]
    
    
    response = client.delete(f'/api/orders/{order1.id}', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'})
    assert response.status_code == 403