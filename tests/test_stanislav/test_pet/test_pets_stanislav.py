from src.assertions import Assertions
from src.http_methods import MyRequests
from data.data_pet import post_add_new_pet
from data.status_code import StatusCode
from data.urls import PetUrls, BASE_URL
import allure


class TestNewPet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Add new pet and check status code of the response")
    def test_post_add_new_pet_has_status_code_200(self):
        headers = {'Content-Type': 'application/json'}
        response = MyRequests.post(BASE_URL+self.link.PET, post_add_new_pet, headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Add new pet and make sure the response is JSON")
    def test_post_add_new_pet_has_json_response(self):
        headers = {'Content-Type': 'application/json'}
        response = MyRequests.post(self.link.PET, post_add_new_pet, headers)
        Assertions.assert_response_has_be_json(response)

    @allure.title("Find pet by ID and check status code of the response")
    def test_get_find_pet_by_id_has_status_code_200(self):
        response = MyRequests.get(self.link.PET_ID, post_add_new_pet)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Find pet by ID and make sure the response is JSON")
    def test_get_add_new_pet_has_json_response(self):
        response = MyRequests.get(self.link.PET_ID, post_add_new_pet)
        Assertions.assert_response_has_be_json(response)
