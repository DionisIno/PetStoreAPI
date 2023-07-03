import allure

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.status_code import StatusCode
from data.urls import PetUrls, BASE_URL
from tests.test_vera.conf import headers, pet_data_set


class TestUpdatePet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Update pet > Status code is 200")
    def test_update_pet_status_code(self, pet_data_set):
        """
        The test updates pet's information with valid data and checks the status code of the response
        """
        pet_data_set["name"] = "new name"
        response = MyRequests.put(self.link.PET, pet_data_set)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        Assertions.assert_json_value_by_name(response, "name", "new name", "Failed to update the pet's name")

    @allure.title("Update pet > Name is updated")
    def test_update_pet_name(self, pet_data_set):
        """
        Test updates the pet's name and checks if it is updated successfully.
        """
        pet_data_set["name"] = "new name"
        response = MyRequests.put(self.link.PET, pet_data_set)
        Assertions.assert_json_value_by_name(response, "name", "new name", "Failed to update the pet's name")
