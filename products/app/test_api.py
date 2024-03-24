import json
import pytest
import pytest_mock
from app import create_app, db
from app.models import Product



@pytest.fixture
def mock_requests_get(mocker):
    def mock_get(url, headers):
        if headers.get('Authorization') == 'Bearer valid_token':
            return mocker.Mock(status_code=200, json=lambda: {'id': 1, 'username': 'test_user'})
        else:
            return mocker.Mock(status_code=401)

    return mocker.patch("app.auth.requests.get", side_effect=mock_get)

@pytest.fixture
def client():
    app = create_app(testing=True)
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()


def test_get_with_valid_token(client, mock_requests_get):
    # Make a request with a valid token
    product1 = Product(name='Product 1', description='Description 1', price=10.0, user_id=1)
    product2 = Product(name='Product 2', description='Description 2', price=20.0, user_id=2)
    db.session.add_all([product1, product2])
    db.session.commit()

    response = client.get('/api/products', headers={'Authorization': 'Bearer valid_token'})

    # Assert that the response status code is 200
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_without_valid_token(client, mock_requests_get):
    # Make a request with a valid token
    product1 = Product(name='Product 1', description='Description 1', price=10.0, user_id=1)
    product2 = Product(name='Product 2', description='Description 2', price=20.0, user_id=1)
    db.session.add_all([product1, product2])
    db.session.commit()

    response = client.get('/api/products')
    assert response.status_code == 401
    # assert len(response.json) == 0


def test_update_func(client, mock_requests_get):
    product1 = Product(name='Product 1', description='Description 1', price=10.0, version=0, user_id=1)
    product2 = Product(name='Product 2', description='Description 2', price=20.0, version=0, user_id=2)
    db.session.add_all([product1, product2])
    db.session.commit()
    data = product1.as_dict()
    data["description"] = "updated"
    response = client.put(f'/api/product/1', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'}, data=json.dumps(data))
    assert response.status_code == 200

    data = product2.as_dict()
    data["description"] = "updated"
    response = client.put(f'/api/product/{product2.id}', headers={'Authorization': 'Bearer valid_token', 'Content-Type': 'application/json'}, data=json.dumps(data))
    assert response.status_code == 404


def test_optimistic_locking_update(client, mock_requests_get):
    product1 = Product(name='Product 1', description='Description 1', price=10.0, version=1, user_id=1)
    product2 = Product(name='Product 2', description='Description 2', price=20.0, version=0, user_id=1)

    db.session.add_all([product1, product2])
    db.session.commit()
    data = product1.as_dict()
    
    data["description"] = "updated"
    data["version"] = 0
    
    response = client.put(f'/api/product/1', headers={'Authorization': 'Bearer valid_token',  'Content-Type': 'application/json'}, data=json.dumps(data))
    assert response.status_code == 409

    data = product2.as_dict()
    data["description"] = "updated"
    data["version"] = 0
    response = client.put(f'/api/product/2', headers={'Authorization': 'Bearer valid_token',  'Content-Type': 'application/json'}, data=json.dumps(data))
    assert response.status_code == 200
    db_product2 = Product.query.filter(Product.id==2).first().as_dict()
    assert response.json == db_product2



def test_retrive_api(client, mock_requests_get):
    product1 = Product(name='Product 1', description='Description 1', price=10.0, version=1,user_id=1)
    product2 = Product(name='Product 2', description='Description 2', price=20.0, version=0, user_id=2)
    db.session.add_all([product1, product2])
    db.session.commit()
    
    response = client.get(f'/api/product/{product1.id}', headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 200
    assert response.json == product1.as_dict()

    response = client.get(f'/api/product/{product2.id}', headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 404


def test_delete_api(client, mock_requests_get):
    product1 = Product(name='Product 1', description='Description 1', price=10.0, version=0, user_id=1)
    product2 = Product(name='Product 2', description='Description 1', price=10.0, version=0, user_id=2)

    db.session.add_all([product1, product2])
    db.session.commit()
    
    response = client.delete(f'/api/product/{product1.id}', headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 204
    # checking against db
    assert Product.query.filter(Product.id==product1.id).first() is None


    response = client.delete(f'/api/product/{product2.id}', headers={'Authorization': 'Bearer valid_token'})
    assert response.status_code == 404
    print(Product.query.all(), "*"*100)
    assert Product.query.filter(Product.id==product2.id).first() is not None

