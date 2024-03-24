import os
import requests

USERS_SERVICE = os.environ.get("USERS_SERVICE")
PRODUCTS_SERVICE = os.environ.get("PRODUCTS_SERVICE")

class Constant:
    @staticmethod
    def get_user_me_et():
        return f'http://{USERS_SERVICE}/api/me'

    @staticmethod
    def get_product_detail_et(product_id):
        return f"http://{PRODUCTS_SERVICE}/api/product/{product_id}"