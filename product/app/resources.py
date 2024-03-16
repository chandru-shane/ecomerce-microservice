from flask import request
from flask_restx import Namespace, Resource
from .extensions import db
from .models import Product
from .api_models import product_model
from .auth import verify_token_with_user_auth

ns = Namespace("api")


@ns.route("/product")
class ProductView(Resource):
    @ns.marshal_list_with(product_model)
    @verify_token_with_user_auth
    def get(self, auth_data):
        return Product.query.all()


    @ns.expect(product_model, validate=True)  # Ensure incoming data matches the model
    @ns.marshal_with(product_model, code=201)  # Marshal output data with the model and response code 201 (Created)
    @verify_token_with_user_auth
    def post(self, auth_data):
        data = request.json  # Get JSON data from the request
        data.pop('id', None)
        product = Product(**data)  # Create a new Product instance with the JSON data
        db.session.add(product)  # Add the product to the database session
        db.session.commit()  # Commit the changes to the database
        return product, 201  # Return the newly created product with status code 201
    


@ns.route("/product/<int:id>")
class ProductDetailView(Resource):
    @ns.marshal_with(product_model)
    def get(self, id):
        product = Product.query.get_or_404(id)
        return product

    @ns.expect(product_model, validate=True)
    @ns.response(code=200, description='Product updated successfully')
    @ns.marshal_with(product_model)
    def put(self, id):
        data = request.json
        product = Product.query.get_or_404(id)
        
        # Check if the provided version matches the current version in the database
        if 'version' not in data or data['version'] != product.version:
            return {'message': 'The product has been updated by another user. Please reload and try again.'}, 409
        
        # Update the product attributes
        for key, value in data.items():
            setattr(product, key, value)
        # Increment the version number
        product.version += 1
        
        db.session.commit()
        return product, 200

    @ns.response(code=204, description='Product deleted successfully')
    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204