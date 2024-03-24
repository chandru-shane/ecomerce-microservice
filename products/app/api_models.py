from flask_restx import fields
from .extensions import api

product_model = api.model("Product", {
    "id":fields.Integer,
    "name":fields.String,
    "description":fields.String,
    "price": fields.String,
    "version": fields.Integer,
    "user_id": fields.Integer,
 })

cud_product_model = api.model("Product", {
    "name":fields.String,
    "description":fields.String,
    "price": fields.String,
    "version": fields.Integer,
 })