import allure
import pytest


from src.assertions import Assertions
from src.http_methods import MyRequests
from data.data_pet import get_pet_by_status
from data.status_code import StatusCode
from data.urls import PetUrls, BASE_URL
from tests.test_vera.data.data_pets import expected_pet_keys
from tests.test_vera.conf import headers, pet_data_set


class TestPet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Find pets by status > Status code is 200")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_01_01_get_pet_by_status_has_status_code_200(self, status):
        """
        This test checks availability of pets by status
        and checks the status code of the response
        :param for status: "available", "pending",  "sold"
        """
        response = MyRequests.get(self.link.BY_STATUS, status)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Find pets by status > Expected number of pets for each status")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_pets_count_by_status(self, status):
        """
        The test checks if the response contains the expected number of pets for each status
        :param for status: "available", "pending",  "sold"
        """
        response = MyRequests.get(self.link.BY_STATUS, data=status)
        data = response.json()
        assert isinstance(data, list)
        assert all(pet['status'] == status['status'] for pet in data)

    @allure.title("Find pets by status > Response content type is JSON")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_response_content_type(self, status):
        """ The test checks if the response content type is JSON """
        response = MyRequests.get(self.link.BY_STATUS, data=status)
        Assertions.assert_response_has_be_json(response)

    @allure.title("Find pets by status > Response headers contain the necessary fields")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_response_headers(self, status):
        """ The test checks if the response cheaders contain the necessary fields"""
        get_pet_by_status_headers = ['access-control-allow-headers', 'access-control-allow-methods',
                                     'access-control-allow-origin',
                                     'content-type', 'content-type', 'date', 'server']
        response = MyRequests.get(self.link.BY_STATUS, data=status)
        for header, value in response.headers.items():
            print(f"{status} - {header}: {value}")
            if header in get_pet_by_status_headers:
                assert header in response.headers, f"Expected header '{header}' not found"
                assert value == get_pet_by_status_headers[
                    header], f"Expected value '{get_pet_by_status_headers[header]}' for header '{header}'"

    @allure.title("Create pet > Expected pet keys in response")
    def test_add_pet_keys_in_response(self, headers, pet_data_set):
        """ The test checks "id" in json response for the created pet """
        response = MyRequests.post(self.link.PET, data=pet_data_set, headers=headers)
        Assertions.assert_response_has_be_json(response)
        Assertions.assert_json_has_keys(response, expected_pet_keys)

    @allure.title("Create pet > Expected pet name in response")
    def test_add_pet_name_in_response(self, headers, pet_data_set):
        """ The test checks pet's name in json response for the created pet """
        response = MyRequests.post(self.link.PET, data=pet_data_set, headers=headers)
        Assertions.assert_response_has_be_json(response)
        Assertions.assert_json_value_by_name(response, 'name', pet_data_set['name'],
                                             "Incorrect pet name in the response")

    @allure.title("Get pet by ID > Status code is 200")
    def test_get_pet_by_id(self, headers, pet_data_set):
        """This test to get pet info by ID and ensures status code is 200"""
        # creating a pet
        response = MyRequests.post(self.link.PET, data=pet_data_set, headers=headers)
        pet_id = response.json()['id']
        url = self.link.PET + f"/{pet_id}"
        # getting response
        response = MyRequests.get(url, headers=headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
