from string import digits

from core.clients.api_client import APIClient
import pytest
from datetime import datetime, timedelta
from faker import Faker


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture()
def booking_dates():
    today = datetime.today()
    checkin_date = today + timedelta(days=10)
    checkout_data = checkin_date + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime('%Y-%m-%d'),
        "checkout": checkout_data.strftime('%Y-%m-%d')
    }


@pytest.fixture()
def generate_random_booking_data(booking_dates):
    faker = Faker()
    firstname = faker.first_mame()
    lastname = faker.lastname()
    totalprice = faker.random_number(digits=3)
    depositpade = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpade": depositpade,
        "additionalneeds": additionalneeds
    }

    return data
