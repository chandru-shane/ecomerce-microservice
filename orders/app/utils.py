import requests
from .constants import Constant
from loguru import logger


def get_product(request, product_id):
    logger.debug("fetching data for product_id=", product_id)
    product_url = Constant.get_product_detail_et(product_id=product_id)
    headers = {"Authorization":f"{request.headers.get('Authorization')}"}
    response = requests.get(product_url, headers=headers)
    # assert response.status_code == 200
    return response.json()