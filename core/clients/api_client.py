from http.client import responses

import requests
import os
from dotenv import load_dotenv
from core.setings.environments import Environment
import allure
from core.clients.endpoints import Endpoints
from core.setings.config import Users, Timeouts

load_dotenv()


class APIClient:
    def __init__(self):
        environments_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environments_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environments_str}")
        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
            return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
            return response.json()

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Expected status 201 but god {response.status_code}"
            return response.status_code

    def auth(self):
        with allure.step("Getting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 201, f"Expected status 201 but god {response.status_code}"
            token = response.json().get("token")
        with allure.step("Updating header  with authorization"):
            self.session.headers.update({"Authorization": f"Bearer{token}"})

    def get_booking_by_id(self):
        with allure.step("Getting booking information for ID"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT_ID}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Expected status 200 but god {response.status_code}"
        with allure.step("Verifying response JSON structure"):
            response_json = response.json()
            expected_structure = {
                "firstname": "Sally",
                "lastname": "Brown",
                "totalprice": 111,
                "depositpaid": True,
                "bookingdates": {
                    "checkin": "2013-02-23",
                    "checkout": "2014-10-23"
                },
                "additionalneeds": "Breakfast"
            }
            assert response_json["firstname"] == expected_structure["firstname"]
            assert response_json["lastname"] == expected_structure["lastname"]
            assert response_json["totalprice"] == expected_structure["totalprice"]
            assert response_json["depositpaid"] == expected_structure["depositpaid"]
            assert response_json["bookingdates"] == expected_structure["bookingdates"]
            assert response_json["additionalneeds"] == expected_structure["additionalneeds"]
        return response_json
