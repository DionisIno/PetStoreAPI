import allure
import json

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.status_code import StatusCode
from data.urls import PetUrls
from tests.test_vera.conf import headers, pet_data_set



class TestCreatePet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Create pet > Status code is 200")
    def test_add_pet_to_store(self, headers, pet_data_set):
        response = MyRequests.post(self.link.PET, pet_data_set, headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Create pet > Response is in json format")
    def test_add_pet_response_format(self, headers, pet_data_set):
        """ The test checks response is in json format for the created pet """
        response = MyRequests.post(self.link.PET, pet_data_set, headers=headers)
        Assertions.assert_response_has_be_json(response)

    @allure.title("Add new pet and make sure the response is JSON")
    def test_post_add_new_pet_has_json_response(self, headers, pet_data_set):
        response = MyRequests.post(self.link.PET, pet_data_set, headers)
        Assertions.assert_response_has_be_json(response)

    @allure.title("Create pet > Expected pet 'id' in response")
    def test_add_pet_id_in_response(self, headers, pet_data_set):
        """ The test checks "id" in json response for the created pet """
        response = MyRequests.post(self.link.PET, pet_data_set, headers=headers)
        try:
            json_response = response.json()
            assert "id" in json_response, "Failed to find 'id' key in the JSON response"
            assert json_response["id"] != 0, "'id' in the JSON response is 0"
        except json.JSONDecodeError:
            assert False, f"""Response is not JSON format. Response text is '{response.text}'"""
