import json
import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture
def client():
    app = create_app(testing=True)
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_get_all_products(client):
    # Add some products to the database
    product1 = Product(name='Product 1', description='Description 1', price=10.0)
    product2 = Product(name='Product 2', description='Description 2', price=20.0)
    db.session.add_all([product1, product2])
    db.session.commit()

    response = client.get('/api/product')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert len(data) == 2
    # Add more assertions based on the expected response data

def test_create_product(client):
    # Define a new product data
    new_product_data = {
        'name': 'New Product',
        'description': 'New Description',
        'price': 30.0
    }

    response = client.post('/api/product', json=new_product_data)
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 201
    assert 'id' in data
    assert data['name'] == new_product_data['name']