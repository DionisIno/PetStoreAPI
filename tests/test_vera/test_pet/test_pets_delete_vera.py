import allure
import pytest

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.status_code import StatusCode
from data.urls import PetUrls
from tests.test_vera.conf import headers, update_headers, pet_data_set
from tests.test_vera.data.data_pets import ExpectedPetsResult as PET


@allure.epic('DELETE: delete pets from the store')
class TestDeletePet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Delete pet > Status code is 200")
    def test_delete_pet_status_code_200(self, pet_data_set):
        """This test case ensures status code is 200 for the successful delete of a pet."""
        pet_data_set["pet_id"] = PET.pet["pet_id"]
        # creating a pet
        response = MyRequests.post(
            self.link.PET,
            data=pet_data_set,
        )
        # deleting the pet and checking the status code is 200
        actual_pet_id = int(response.json()["id"])
        response = MyRequests.delete(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set,
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Delete pet > Status code is 404 for second attempt to delete")
    def test_delete_pet_twice_status_code_404(self, pet_data_set):
        """This test case ensures status code is 200 to the second attempt to delete the same pet."""
        pet_data_set["pet_id"] = PET.pet["pet_id"]
        # creating a pet
        response = MyRequests.post(
            self.link.PET,
            data=pet_data_set,
            # headers=headers
        )
        # deleting the pet
        actual_pet_id = int(response.json()["id"])
        response = MyRequests.delete(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set,
        )
        # attempting to delete the pet again and checking the status code is 404
        response = MyRequests.delete(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set,
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)

    @allure.title("Delete pet > Status code is 404 if delete with non-existing ID")
    def test_delete_pet_with_non_existing_id_status_code_404(self, pet_data_set):
        """This test case ensures status code is 404 for the attempt to delete a pet with non-existing ID."""
        pet_id = -1
        response = MyRequests.delete(
            self.link.PET + f"/{pet_id}",
            data=pet_data_set
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)

    @allure.title("Delete pet > Status code is 404 if delete with invalid ID")
    def test_delete_pet_with_invalid_id_status_code_404(self, pet_data_set):
        """This test case ensures status code is 404 for the attempt to delete a pet with invalid ID."""
        pet_data_set["pet_id"] = PET.pet["pet_id"]
        response = MyRequests.delete(
            self.link.PET + f"/{PET.pet['pet_id']}",
            data=pet_data_set
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)
