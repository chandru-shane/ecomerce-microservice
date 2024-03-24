from flask import request
from flask_restx import Namespace, Resource, abort
from .extensions import db
from .models import Order
from .api_models import order_model
from .auth import verify_token_with_user_auth
from .utils import get_product
from loguru import logger

ns = Namespace("api")


@ns.route("/orders")
class OrderView(Resource):
    @verify_token_with_user_auth
    @ns.marshal_list_with(order_model)
    def get(self, auth_data):
        orders =  Order.query.filter(Order.user_id == auth_data.get('id')).all()
        return orders

    @verify_token_with_user_auth
    @ns.expect(order_model, validate=True)
    @ns.response(code=201, description='Order created successfully')
    @ns.marshal_with(order_model)
    def post(self, auth_data):
        data = request.json
        
        if data["user_id"] != auth_data.get("id"):
            abort(403, "You're not allowed to do this")
        
        product_data = get_product(request,data['product_id'])


        if product_data['price'] != data['price']:
            abort(409, "Please try with the updated product data")
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        return order, 201

@ns.route("/orders/<int:id>")
class OrderDetailView(Resource):
    @verify_token_with_user_auth
    @ns.marshal_with(order_model)
    def get(self, id, auth_data):
        order = Order.query.filter(Order.id==id, Order.user_id==auth_data.get("id")).first()
        if not order:
            abort(403, "You don't have access!")
        return order

    @verify_token_with_user_auth
    @ns.expect(order_model, validate=True)
    @ns.response(code=200, description='Order updated successfully')
    @ns.marshal_with(order_model)
    def put(self, id, auth_data):
        data = request.json
        order = Order.query.filter(Order.id==id, Order.user_id==auth_data.get("id")).first()
        if not order:
            abort(403, "You don't have access!")
        for key, value in data.items():
            if key in ["product_id", "user_id", "price", "id", "created", "updated"]: # user should not create once order placed
                continue
            setattr(order, key, value)
        db.session.commit()
        return order, 200
    
    @verify_token_with_user_auth
    @ns.response(code=204, description='Order deleted successfully')
    def delete(self, id, auth_data):
        order = Order.query.filter(Order.id==id, Order.user_id==auth_data.get("id")).first()
        if not order:
            abort(403, "You don't have access!")
        db.session.delete(order)
        db.session.commit()
        return '', 204
