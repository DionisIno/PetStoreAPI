import json
from requests import Response
from src.http_methods import MyRequests
from data.data_user import user_json, user_json_without_id, headers
from data.urls import UserUrls


class Assertions:
    @staticmethod
    def assert_code_status(response: Response, expected_status_code: object) -> object:
        actual_status_code = response.status_code
        assert actual_status_code == expected_status_code, \
            f"Unexpected status code. Expected: {expected_status_code}. Actual: {actual_status_code}"

    @staticmethod
    def assert_status_reason(response: Response, expected_status_reason):
        actual_status_reason = response.reason
        assert actual_status_reason == expected_status_reason, \
            f"Unexpected status reason. Expected: {expected_status_reason}. Actual: {actual_status_reason}"

    @staticmethod
    def assert_response_has_be_json(response: Response):
        assert 'application/json' in response.headers.get('Content-Type', ''), \
            "Error: Response is not in JSON format"

    @staticmethod
    def assert_response_has_header(response: Response, header_key, header_value):
        assert header_key in response.headers.keys(), \
            f"Error: Response doesn't have header {header_key}"
        assert header_value == response.headers.get(header_key), \
            f"Error: Response doesn't have value {header_value} in header {header_key}"

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"""Response is not JSON format. Response text is '{response.text}'"""
        assert name in response_json, f"""response JSON doesn't have key '{name}'"""
        assert response_json[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"""Response is not JSON format. Response text is '{response.text}'"""
        assert name in response_json, f"""response JSON doesn't have key '{name}'"""

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"""Response is not JSON format. Response text is '{response.text}'"""
        for name in names:
            assert name in response_json, f"""response JSON doesn't have key '{name}'"""

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"""Response is not JSON format. Response text is '{response.text}'"""
        assert name not in response_json, f"""response JSON shouldn't have key '{name}', but it's present"""

    @staticmethod
    def assert_json_has_not_keys(response: Response, names: list):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"""Response is not JSON format. Response text is '{response.text}'"""
        for name in names:
            assert name not in response_json, f"""response JSON shouldn't have key '{name}', but it's present"""

    @staticmethod
    def assert_json_value_has_positive_number_only(response: Response, key):
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            assert False, f"""Response is not JSON format. Response text is '{response.text}'"""
        try:
            key_to_number = int(response_json[key])
        except ValueError:
            assert False, f"""Value has not only digits. Value is '{response_json[key]}'"""
        assert key_to_number >= 0, f"""Value is not positive number. Value is '{key_to_number}'"""

    @staticmethod
    def assert_server_response_time_satisfies_the_requirements(number_of_calls, requirements_time):
        """
        :param int number_of_calls: number of api calls
        :param int or float requirements_time: time in seconds

        NOTE: response.elapsed measures the time between sending the request and finishing parsing the response headers,
        not until the full response contents has been transferred. If you want to measure that time, you need to measure
        it yourself:
            start = time.perf_counter()
            response = requests.post(url, data=post_fields, timeout=timeout)
            request_time = time.perf_counter() - start
        """
        response_times_list = []
        for x in range(number_of_calls):
            response = MyRequests.post(UserUrls.CREATE_USER, user_json)
            response_times_list.append(response.elapsed.total_seconds())
        average_time = sum(response_times_list)/len(response_times_list)
        assert average_time <= requirements_time, \
            f"Server response time {average_time} sec. is longer than requirements time {requirements_time} sec."
