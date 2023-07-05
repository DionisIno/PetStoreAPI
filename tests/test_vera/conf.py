import pytest


@pytest.fixture
def headers():
    return {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

@pytest.fixture
def update_headers():
    return {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

@pytest.fixture
def pet_data_set():
    return {
        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }


@pytest.fixture
def config_user_data():
    return [
            {
                "id": 0,
                "username": "string",
                "firstName": "string",
                "lastName": "string",
                "email": "string",
                "password": "string",
                "phone": "string",
                "userStatus": 0
            }
        ]
