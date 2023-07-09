import allure

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.status_code import StatusCode
from data.urls import PetUrls, BASE_URL
from tests.test_vera.conf import headers, pet_data_set
from tests.test_vera.data.data_pets import ExpectedPetsResult as PET


@allure.epic('PUT: Update pets in the store')
class TestUpdatePet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Update pet > Status code is 200")
    def test_update_pet_status_code(self):
        """
        The test updates pet's information with valid data and checks the status code is 200
        """
        data = PET.update_pet_info
        response = MyRequests.put(
            self.link.PET,
            data=data
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Update pet > Pet's info is updated successfully")
    def test_update_pet_info_successful(self):
        """
        Test updates the pet's info and checks if it is updated successfully.
        """
        data = PET.update_pet_info
        response = MyRequests.put(
            self.link.PET,
            data=data
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        pet_info = response.json()
        # Verify that the updated values match the expected values
        assert pet_info['name'] == data['name'], "Failed to update the pet's name"
        assert pet_info['photoUrls'] == data['photoUrls'], "Failed to update the pet's photo"
        assert pet_info['category']['id'] == data['category']['id'], "Failed to update the pet's category ID"
        assert pet_info['category']['name'] == data['category']['name'], "Failed to update the pet's category name"
        assert pet_info['tags'] == data['tags'], "Failed to update the pet's tags"
        assert pet_info['status'] == data['status'], "Failed to update the pet's status"

    @allure.title("Update a deleted pet > Status code is 405 - Method Not Allowed")
    def test_update_deleted_pet_status_code_405(self, pet_data_set):
        '''The test checks the status code is 405 when attempting to update a deleted pet'''
        pet_data_set["pet_id"] = PET.pet["pet_id"]
        # Creating a pet
        response = MyRequests.post(
            self.link.PET,
            data=pet_data_set
        )
        # Deleting the pet and ensuring the status code is 200
        actual_pet_id = int(response.json()["id"])
        response = MyRequests.delete(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        # Sending the GET request to get the pet info and ensuring the status code is 404 (not found)
        response = MyRequests.get(self.link.PET + f"/{actual_pet_id}")
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)
        # Sending the PUT request to update information for the pet
        data = PET.update_pet_info
        data["id"] = actual_pet_id
        response = MyRequests.put(BASE_URL + self.link.PET, data)
        # Asserting that the status code is 405 (not found)
        try:
            Assertions.assert_code_status(response, self.status_code.STATUS_CODE_405)
        except AssertionError as error:
            print("Expected 405 status code, but received:", response.status_code)
            assert False
