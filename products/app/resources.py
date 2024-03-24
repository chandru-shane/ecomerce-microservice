from flask import request, jsonify
from flask_restx import Namespace, Resource
from .extensions import db
from .models import Product
from .api_models import product_model
from .auth import verify_token_with_user_auth
from loguru import logger
from flask_restx import abort
from werkzeug.exceptions import NotFound



ns = Namespace("api")

from prometheus_client import Counter
view_metric = Counter('view', 'Product view', ['user'])

detail_view_metric = Counter('detail_view', 'Product Detail view', ['product'])


@ns.route("/products")
class ProductView(Resource):
    @verify_token_with_user_auth
    @ns.marshal_list_with(product_model)
    def get(self, auth_data):
        view_metric.labels(user=auth_data.get("id")).inc()
        logger.info("GET request received for products endpoint, New world")
        product =  Product.query.filter(Product.user_id==auth_data.get("id")).all()
        return product


    @verify_token_with_user_auth
    @ns.expect(product_model, validate=True)
    @ns.marshal_with(product_model, code=201)
    def post(self, auth_data):
        data = request.json 
        data.pop('id', None)
        data["user_id"] = auth_data.get('id')
        product = Product.query.filter(Product.name==data.get("name")).first()
        if product: abort(400, "Use different name")
        product = Product(**data) 
        db.session.add(product)
        db.session.commit()
        return product, 201
    


@ns.route("/product/<int:id>")
class ProductDetailView(Resource):
    @verify_token_with_user_auth
    @ns.marshal_with(product_model)
    def get(self, id, auth_data):
        detail_view_metric.labels(product=id).inc()
        try:
            product = Product.query.filter_by(id=id, user_id=auth_data['id']).first_or_404()
        except NotFound:
            return jsonify({"error": "Product not found for the given id and user_id"}), 404

        return product

    @verify_token_with_user_auth
    @ns.expect(product_model, validate=True)
    @ns.response(code=200, description='Product updated successfully')
    @ns.marshal_with(product_model)
    def put(self, id, auth_data):
        data = request.json
        try:
            product = Product.query.filter_by(id=id, user_id=auth_data['id']).first_or_404()
        except NotFound:
            return jsonify({"error": "Product not found for the given id and user_id"}), 404
        
        product_name = Product.query.filter(Product.name==data.get("name")).first()
        if product_name and product.id != id: abort(400, "Use different name")
        
        if data.get("user_id") and data.get("user_id") != auth_data.get("id"):
            abort(403, "You don't have permissin to do this")
        
        if 'version' not in data or data['version'] != product.version:
            print(data, product.version)
            return {'message': 'The product has been updated by another user. Please reload and try again.'}, 409
        
        for key, value in data.items():
            if key in ["updated", "created"]:
                continue
            setattr(product, key, value)
        product.version += 1
        
        db.session.commit()
        return product, 200

    @verify_token_with_user_auth
    @ns.response(code=204, description='Product deleted successfully')
    def delete(self, id, auth_data):
        try:
            product = Product.query.filter_by(id=id, user_id=auth_data['id']).first_or_404()
            print(product, "printing from resources")
        except NotFound:
            abort(404)
        db.session.delete(product)
        db.session.commit()
        return '', 204