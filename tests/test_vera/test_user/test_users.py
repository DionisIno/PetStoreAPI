import allure
import pytest
import requests

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.status_code import StatusCode
from tests.test_vera.data import data_user
from data.urls import UserUrls, BASE_URL
from tests.test_vera.conf import headers, config_user_data

class TestUser:
    status_code = StatusCode()
    link = UserUrls

    @allure.title("Create User > Status code is 200 for successful user creation")
    def test_create_users_with_array_status_200(self, headers, config_user_data):
        """
        Positive Test: a user can be successfully created with valid data.
        The test checks if the status code returned for a successful user creation is 200.
        """
        url = self.link.CREATE_USER
        response = MyRequests.post(url, data=config_user_data, headers=headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Create User > JSON response is correct")
    def test_create_users_with_array_json_format(self, headers, config_user_data):
        """
        Positive Test: a user can be successfully created with valid data.
        The test checks if the JSON response is correct when a user is successfully created
        """
        url = self.link.CREATE_USER
        response = MyRequests.post(url, data=config_user_data, headers=headers)
        Assertions.assert_response_has_be_json(response)
        Assertions.assert_json_has_keys(response, data_user.success_user_response)

    @allure.title("Create User > headers are correct")
    def test_create_users_with_array_headers(self, headers, config_user_data):
        """
        Positive Test: a user can be successfully created with valid data.
        The status code of 200 is received when a user is successfully created
        """
        response = MyRequests.post(self.link.CREATE_USER, data=config_user_data, headers=headers)
        for header, value in response.headers.items():
            print(f"{header}: {value}")
            assert header in response.headers, f"Expected header '{header}' not found"

    @allure.title("Get User by user name> Status code is 200 and user data are correct")
    def test_get_user_by_username_status_code_200(self, headers):
        """
        Test case to verify successful retrieval of a user by their username. The status code of 200 is received.
        """
        create_user_url = BASE_URL + self.link.CREATE_USER
        get_user_url = BASE_URL + self.link.USER
        username = "testuser"
        data = [
            {
                "username": username,
            }
        ]
        # Create a user
        response = requests.post(create_user_url, json=data, headers=headers)
        # response = MyRequests.post(BASE_URL + self.link.CREATE_USER, json=data, headers=headers) # doesn't work
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        # Retrieve the user
        response = requests.get(get_user_url + username, headers=headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Get User by user name> User data are correct")
    def test_get_user_by_username_correct_data(self, headers):
        """
        Test case to verify the retrieved user's information matches the expected data
        """
        username = "newuser"
        email = "newuser@test.com"
        data = [
            {
                "id": 92233720,
                "username": username,
                "firstName": "Joe",
                "lastName": "Smith",
                "email": email,
                "password": "pAssword",
                "phone": "1234567890",
                "userStatus": 0
            }
        ]
        # Create a user
        response = requests.post(BASE_URL + self.link.CREATE_USER, json=data, headers=headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        # Retrieve the user
        response = requests.get(BASE_URL + self.link.USER + username, headers=headers)
        actual_user_data = response.json()
        Assertions.assert_json_value_by_name(response, "username", username,
                    f"Unexpected username. Expected: {username}, Actual: {actual_user_data['username']}")
        Assertions.assert_json_has_keys(response, data_user.expected_user_fields)
        assert actual_user_data == data[0] # assert all values

    @allure.title("Get User by user name> User data are correct")
    def test_get_user_by_username_json_has_keys(self, headers):
        """
        Test case to verify the retrieved user's information json has expected keys
        """
        data = data_user.user_data_set
        username = "newuser"
        data[0]["username"] = username
        response = requests.post(BASE_URL + self.link.CREATE_USER, json=data, headers=headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        # Retrieve the user
        response = requests.get(BASE_URL + self.link.USER + username, headers=headers)
        actual_user_data = response.json()
        Assertions.assert_json_has_keys(response, data_user.expected_user_fields)

    @allure.title("Get User by user name> Error response for invalid username")
    def test_get_user_by_username_invalid_username_status_code(self, config_user_data, headers):
        """
        Test case to verify error response when invalid request data of username is sent.
        """
        username = "invaliduser"
        url = BASE_URL + self.link.USER + username
        response = requests.get(url, headers=headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)

    @allure.title("Get User by user name> Error response for invalid username")
    def test_get_user_by_username_invalid_username_error(self, config_user_data, headers):
        """
        Test case to verify error message in response when invalid request data of username is sent.
        """
        username = "invaliduser"
        url = BASE_URL + self.link.USER + username
        response = requests.get(url, headers=headers)
        expected_error = {
            "code": 1,
            "type": "error",
            "message": "User not found"
        }
        error_data = response.json()
        assert error_data == expected_error, \
            f"Unexpected error data. Expected: {expected_error}, Actual: {error_data}"

    @allure.title("Get User by user name> Srarus code is 405 for missing username")
    def test_get_user_by_username_missing_username_status_code_405(self, headers):
        """
        Test case to verify status code is 405 for response when no username is provided.
        """
        response = requests.get(url = BASE_URL + self.link.USER, headers=headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_405)

    @allure.title("Get User by user name> Error response for missing username")
    def test_get_user_by_username_missing_username_error(self, headers):
        """
        Test case to verify error response when no username is provided.
        """
        response = requests.get(BASE_URL + self.link.USER, headers=headers)
        expected_error = {
            "code": 405,
            "type": "unknown",
        }
        error_data = response.json()
        assert error_data == expected_error, "Error is missing or incorrect"
