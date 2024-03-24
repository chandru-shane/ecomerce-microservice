import os
import requests
from flask import request
from functools import wraps

USERS_SERVICE = os.environ.get('USERS_SERVICE')
def verify_token_with_user_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Get the JWT token from the request headers
        token = request.headers.get('Authorization', None)
        if token is None:
            return {'message': 'Unauthorized. Please provide a valid access token'}, 401
        token = token.split(' ')[1]

        # Make a request to the user_auth microservice API to verify the token
        response = requests.get(f'http://{USERS_SERVICE}/api/me', headers={'Authorization': f'Bearer {token}'})        
        
        # Check if the token is valid based on the response status code
        if response.status_code == 200:
            auth_data = response.json()
            
            return func(auth_data=auth_data, *args, **kwargs)  # Proceed with the original function
        else:
            return {'message': 'Unauthorized. Please provide a valid access token'}, 401

    return decorated_function