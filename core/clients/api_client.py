from http.client import responses

import requests
import os
from dotenv import load_dotenv
from core.setings.environments import Environment
load_dotenv()

class APIClient:
    def __init__(self):
        environments_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environments_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environments_str}")
        self.base_url = self.get_base_url(environment)
        self.headers = {
            'Content-Type' : 'application/json'
        }
    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")
    def get(self, endpoint, params=None, status_code = 200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert  response.status_code == status_code
            return response.json()
    def post(self, endpoint, data=None, status_code = 200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert  response.status_code == status_code
            return response.json()