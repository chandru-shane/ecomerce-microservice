import os
import requests
from flask import request
from functools import wraps


USERS_SERVICE = os.environ.get("USERS_SERVICE")

def verify_token_with_user_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token is None:
            return {'message': 'Unauthorized. Please provide a valid access token'}, 401
        token = token.split(' ')[1]
        #TODO: Change to env
        response = requests.get(f'http://{USERS_SERVICE}/api/me', headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 200:
            auth_data = response.json()
            
            return func(auth_data=auth_data, *args, **kwargs)  
        else:
            return {'message': 'Unauthorized. Please provide a valid access token'}, 401

    return decorated_function