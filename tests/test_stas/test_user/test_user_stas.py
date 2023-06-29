import pytest
from src.http_methods import MyRequests
from data.urls import UserUrls
from src.assertions import Assertions
from data.data_user import user_json, user_json_without_id, headers
import allure


class TestUser:
    url = UserUrls

    @allure.title("POST /user. Verify that HTTP protocol version is 1.1.")
    def test_01_verify_http_protocol_version(self):
        """This test verify HTTP protocol version"""
        response = MyRequests.post(self.url.CREATE_USER, user_json)
        assert response.raw.version == 11, "HTTP protocol version is not 1.1"

    @allure.title("POST /user. Verify that server respond with '200 OK' status when creating user.")
    def test_02_create_user_is_successful(self):
        """This test verify that server respond with "200 OK" status when creating user"""
        response = MyRequests.post(self.url.CREATE_USER, user_json)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_status_reason(response, "OK")

    @allure.title("POST /user. Verify that server respond with '200 OK' status when creating user without 'id' key in request body.")
    def test_03_create_user_without_id_is_successful(self):
        """This test verify that server respond with "200 OK" status when creating user without 'id' key in request body"""
        response = MyRequests.post(self.url.CREATE_USER, user_json_without_id)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_status_reason(response, "OK")

    @allure.title("POST /user. Verify that server respond with valid JSON when creating user.")
    def test_04_create_user_has_valid_response_json(self):
        """This test verify that server respond with valid JSON when creating user"""
        response = MyRequests.post(self.url.CREATE_USER, user_json)
        Assertions.assert_json_value_by_name(response, "code", 200,
                                             "response JSON doesn't have value '200' with key 'code'")
        Assertions.assert_json_value_by_name(response, "type", "unknown",
                                             "response JSON doesn't have value 'unknown' with key 'type'")
        Assertions.assert_json_value_has_positive_number_only(response, "message")

    @allure.title("POST /user. Verify that server respond with valid JSON when creating user without 'id' key in request body.")
    def test_05_create_user_without_id_has_valid_response_json(self):
        """This test verify that server respond with valid JSON when creating user without 'id' key in request body"""
        response = MyRequests.post(self.url.CREATE_USER, user_json_without_id)
        Assertions.assert_json_value_by_name(response, "code", 200,
                                             "response JSON doesn't have value '200' with key 'code'")
        Assertions.assert_json_value_by_name(response, "type", "unknown",
                                             "response JSON doesn't have value 'unknown' with key 'type'")
        Assertions.assert_json_value_has_positive_number_only(response, "message")

    @allure.title("POST /user. Verify that user 'id' in request JSON is equal to user 'id' in response JSON when creating user.")
    def test_07_user_id_in_request_json_equals_user_id_in_response_json(self):
        """This test verify that user 'id' in response JSON is equal to user 'id' in response JSON when creating user"""
        response = MyRequests.post(self.url.CREATE_USER, user_json)
        request_id = user_json["id"]
        response_id = int(response.json()["message"])
        assert request_id == response_id

    @allure.title("POST /user. Verify that response has required headers when creating user")
    @pytest.mark.parametrize("header", headers)
    def test_08_create_user_has_required_headers(self, header):
        """This test verify that that response has required headers when creating user
        :param header: "Content-Type" : "application/json", "Transfer-Encoding" : "chunked",
                       "Connection" : "keep-alive", "Access-Control-Allow-Origin" : "*"
        """
        response = MyRequests.post(self.url.CREATE_USER, user_json)
        Assertions.assert_response_has_header(response, header[0], header[1])

    @allure.title("POST /user. Verify that server response time satisfies the requirements when creating user.")
    def test_09_create_user_response_time_satisfies_the_requirements(self):
        """This test verify that server response time satisfies the requirements when creating user"""
        Assertions.assert_server_response_time_satisfies_the_requirements(10, 1)
