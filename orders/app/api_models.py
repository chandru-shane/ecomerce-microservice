from flask_restx import fields
from .extensions import api
from flask_restx import fields

order_model = api.model("Order", {
    "id": fields.Integer,
    "product_id": fields.Integer,
    "user_id": fields.Integer,
    "price": fields.String,  # Adjust as necessary
    "quantity": fields.Integer,
    "status": fields.String(enum=['pending', 'on_the_way', 'delivered']),
    "expected_delivery_time": fields.DateTime,
    "updated_at": fields.DateTime,
    "created_at": fields.DateTime
})