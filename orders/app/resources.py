from flask import request
from flask_restx import Namespace, Resource, abort
from .extensions import db
from .models import Order
from .api_models import order_model
from .auth import verify_token_with_user_auth

ns = Namespace("api")


@ns.route("/orders")
class OrderView(Resource):
    @verify_token_with_user_auth
    @ns.marshal_list_with(order_model)
    def get(self, auth_data):
        return Order.query.filter(Order.user_id == auth_data.get('id')).all()

    @verify_token_with_user_auth
    @ns.expect(order_model, validate=True)
    @ns.response(code=201, description='Order created successfully')
    @ns.marshal_with(order_model)
    def post(self, auth_data):
        data = request.json
        if data["user_id"] != auth_data.get("id"):
            abort(403, "You're not allowed to do this")
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        return order, 201

@ns.route("/orders/<int:id>")
class OrderDetailView(Resource):
    @ns.marshal_with(order_model)
    def get(self, id):
        order = Order.query.get_or_404(id)
        return order

    @ns.expect(order_model, validate=True)
    @ns.response(code=200, description='Order updated successfully')
    @ns.marshal_with(order_model)
    def put(self, id):
        data = request.json
        order = Order.query.get_or_404(id)
        for key, value in data.items():
            setattr(order, key, value)
        db.session.commit()
        return order, 200

    @ns.response(code=204, description='Order deleted successfully')
    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return '', 204