from flask_restx import fields
from .extensions import api

product_model = api.model("Product", {
    "id":fields.Integer,
    "name":fields.String,
    "description":fields.String,
    "price": fields.String
 })