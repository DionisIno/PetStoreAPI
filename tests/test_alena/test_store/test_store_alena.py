import pytest
from data.status_code import StatusCode
from data.urls import BASE_URL
import requests
import allure


class TestStore:
    status_code = StatusCode()

    @allure.title("Check url for request and get status code of the response")
    def test_get_where_am_i_and_is_status_code_equal_to_200_here(self):
        """This is my first API test. I'm just trying to figure out if I'm in the right place."""
        response = requests.get("https://petstore.swagger.io")
        expected_status_code = self.status_code.STATUS_CODE_200
        actual_status_code = response.status_code
        print(f"""\nURL: {response.url}\nActual status code: {response.status_code} \n""")
        assert actual_status_code == expected_status_code
