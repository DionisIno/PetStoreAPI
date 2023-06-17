import json

import allure
import pytest
import requests

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.status_code import StatusCode
from tests.test_vera.data.urls import BASE_URL, UserUrls
from tests.test_vera.data.data_user import expected_user_fields
from tests.test_vera.fixtures import headers, user_data

class TestUser:
    status_code = StatusCode()
    link = UserUrls

    @allure.title("Create User > Status code is 200 for successful user creation")
    def test_create_users_with_array(self, headers, user_data):
        """
        Positive Test: a user can be successfully created with valid data.
        The test checks if the status code returned for a successful user creation is 200.
        """
        url = self.link.USER
        print(self.link.USER)
        # json_data = json.dumps(user_data)
        response = MyRequests.post(url, data=user_data, headers=headers)
        # print(" username", username=response.json()['username'])
        print(response.status_code)
        print(response.json())
        print("Response headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Create User > JSON response is correct")
    def test_create_users_with_array(self, headers, user_data):
        """
        Positive Test: a user can be successfully created with valid data.
        The test checks if the JSON response is correct when a user is successfully created
        """
        url = self.link.USER
        # json_data = json.dumps(user_data)
        response = MyRequests.post(url, data=user_data, headers=headers)

        print(response.json())
        print(self.link.USER)

        Assertions.assert_response_has_be_json(response)
        assert response.json() == {
                "code": 200,
                "type": "unknown",
                "message": "ok"
            }

    @allure.title("Create User > headers are correct")
    def test_create_users_with_array(self, headers, user_data):
        """
        Positive Test: a user can be successfully created with valid data.
        The test checks if the status code returned for a successful user creation is 200.
        a status code of 200 is received when a user is successfully created
        """
        url = self.link.USER
        response = MyRequests.post(url, data=json.dumps(user_data), headers=headers)

        print(response.status_code)
        print(response.json())
        print(url)
        print("Response headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
            assert header in response.headers, f"Expected header '{header}' not found"
        # Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Get User by user name> Status code is 200 and user data are correct")
    def test_get_user_by_username_success(self, headers):
        """
        Test case to verify successful retrieval of a user by their username.
        """
        username = "testuser"
        # url = f"https://petstore.swagger.io/v2/user/{username}"
        url = self.link.GET_USER + username

        create_user_url = "https://petstore.swagger.io/v2/user/createWithArray"
        data = [
            {
                "id": 0,
                "username": username,
                "firstName": "string",
                "lastName": "string",
                "email": "string",
                "password": "string",
                "phone": "string",
                "userStatus": 0
            }
        ]
        response = requests.post(create_user_url, json=data, headers=headers)
        assert response.status_code == 200, f"Failed to create user. Status code: {response.status_code}"

        # Perform the GET request to retrieve the user
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, \
            f"Unexpected status code. Expected: 200, Actual: {response.status_code}"


    @allure.title("Get User by user name> User data are correct")
    def test_get_user_by_username_2(self, headers, user_data):
        """
        Test case to verify the retrieved user's information matches the expected data
        """
        username = "testuser2"
        url = self.link.GET_USER + username

        create_user_url = "https://petstore.swagger.io/v2/user/createWithArray"
        response = requests.post(create_user_url, json=user_data, headers=headers)
        assert response.status_code == 200, f"Failed to create user. Status code: {response.status_code}"

        # Perform the GET request to retrieve the user
        response = requests.get(url, headers=headers)

        assert response.status_code == 200, \
            f"Unexpected status code. Expected: 200, Actual: {response.status_code}"

        # Verify the retrieved user's information matches the expected data
        user_data = response.json()
        assert user_data["username"] == username, \
            f"Unexpected username. Expected: {username}, Actual: {user_data['username']}"

    @allure.title("Get User by user name> Error response for invalid username")
    def test_get_user_by_username_invalid_username_status_code(self, user_data, headers):
        """
        Test case to verify error response when invalid request data of username is sent.
        """
        username = "invaliduser"
        url = f"https://petstore.swagger.io/v2/user/{username}"
        response = requests.get(url, headers=headers)
        print(response.status_code)
        Assertions.assert_code_status(response, 404)
    @allure.title("Get User by user name> Error response for invalid username")
    def test_get_user_by_username_invalid_username_error(self):
        """
        Test case to verify error message in response when invalid request data of username is sent.
        """
        username = "invaliduser"
        url = f"https://petstore.swagger.io/v2/user/{username}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        expected_error = {
            "code": 1,
            "type": "error",
            "message": "User not found"
        }
        error_data = response.json()
        print(response.json())
        assert error_data == expected_error, \
            f"Unexpected error data. Expected: {expected_error}, Actual: {error_data}"

    @allure.title("Get User by user name> Error response for missing username")
    def test_get_user_by_username_missing_username(self, headers):
        """
        Test case to verify error response when no username is provided.
        """
        url = "https://petstore.swagger.io/v2/user/"
        response = requests.get(url, headers=headers)
        assert response.status_code == 405, \
            f"Unexpected status code. Expected: 405, Actual: {response.status_code}"
        expected_error = {
            "code": 405,
            "type": "unknown",
        }
        error_data = response.json()
        print(response.json())
        assert error_data == expected_error, "Error is missing or incorrect"

