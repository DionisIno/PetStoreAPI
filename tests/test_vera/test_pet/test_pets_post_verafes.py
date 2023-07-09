import allure
import pytest

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.status_code import StatusCode
from data.urls import PetUrls
from tests.test_vera.conf import headers, update_headers, pet_data_set
from tests.test_vera.data.data_pets import ExpectedPetsResult as PET


@allure.epic('POST: Add a new pet to the store')
class TestCreatePet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Create pet > Status code is 200")
    def test_add_pet_to_store(self, headers, pet_data_set):
        """The test checks status code is 200 for the created pet"""
        response = MyRequests.post(
            self.link.PET,
            pet_data_set,
            headers
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Create pet > Response is in json format")
    def test_add_pet_response_is_json_format(self, headers, pet_data_set):
        """The test checks response is in json format for the created pet """
        response = MyRequests.post(
            self.link.PET,
            pet_data_set,
            headers=headers
        )
        Assertions.assert_response_has_be_json(response)

    @allure.title("Create pet > Expected pet keys in response")
    def test_add_pet_keys_in_response(self, headers, pet_data_set):
        """The test checks "id" in json response for the created pet """
        response = MyRequests.post(
            self.link.PET,
            data=pet_data_set,
            headers=headers
        )
        Assertions.assert_json_has_keys(response, PET.expected_pet_keys)

    @allure.title("Create pet > Expected pet name in response")
    def test_add_pet_name_in_response(self, headers, pet_data_set):
        """ The test checks pet's name in json response for the created pet """
        response = MyRequests.post(
            self.link.PET,
            data=pet_data_set,
            headers=headers
        )
        Assertions.assert_json_value_by_name(response, "name", pet_data_set["name"],
                                             "Incorrect pet name in the response")

    @allure.title("Create pet > Expected pet 'ID' in response")
    def test_add_pet_id_in_response(self, headers, pet_data_set):
        """ The test checks "ID" in json response for the created pet """
        pet_data_set['id'] = PET.pet["pet_id"]
        response = MyRequests.post(
            self.link.PET,
            pet_data_set,
            headers=headers)
        actual_pet_id = int(response.json()["id"])
        Assertions.assert_json_value_by_name(response, "id", actual_pet_id,
                                             "Incorrect pet id in the response")


@allure.epic('POST: Update a pet in the store with form data')
class TestUpdatePet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Update pet > Status code is 200")
    def test_update_pet_info_status_code(self, headers, update_headers, pet_data_set):
        """This test case ensures status code is 200 for the successful update of a pet's information."""
        pet_data_set["name"] = PET.pet["pet_name"]
        pet_data_set["status"] = PET.pet["pet_id"]
        # Creating a pet
        response = MyRequests.post(
            self.link.PET,
            pet_data_set,
            headers=headers
        )
        # Updating the pet and checking the status code is 200
        actual_pet_id = int(response.json()["id"])
        response = MyRequests.post(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set,
            headers=update_headers
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Update pet > Response returns correct updated info")
    @pytest.mark.parametrize("name, expected_value, error_message", PET.expected_pet_names_keys_positive)
    def test_update_pet_info_is_correct(self, pet_data_set, headers, update_headers,
                                        name, expected_value, error_message):
        """
        This test case validates the successful update of a pet's information
        and ensures they have the expected values.
        :param for name: "code", "type", "message" (keys)
        :param for expected_value: 200, "unknown", pet_id
        :param for error_message: "Response JSON doesn't have key {name}"
        """
        pet_data_set["id"] = PET.pet["pet_id"]
        pet_data_set["name"] = PET.pet["pet_name"]
        pet_data_set["status"] = PET.pet["pet_status"]
        # Creating a pet
        response = MyRequests.post(
            self.link.PET,
            pet_data_set,
            headers=headers
        )
        actual_pet_id = int(response.json()["id"])
        # Updating the pet and checking all keys
        response = MyRequests.post(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set,
            headers=update_headers
        )
        Assertions.assert_json_value_by_name(response, name, expected_value, error_message)

    @allure.title("Update pet with non-existing ID > status code is 404")
    def test_update_pet_info_with_invalid_id_status_code_404(self, pet_data_set, headers, update_headers):
        """This test case ensures status code is 404 for a non-existing ID in the update of a pet's information."""
        pet_data_set["name"] = PET.pet["pet_name"]
        pet_data_set["status"] = PET.pet["pet_status"]
        # Creating a pet
        MyRequests.post(
            self.link.PET,
            pet_data_set,
            headers=headers
        )
        # Updating the pet with non-existing ID
        pet_id = -1
        response = MyRequests.post(
            self.link.PET + f"/{pet_id}",
            pet_data_set, headers=update_headers
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)

    @allure.title("Update pet with invalid id > Response JSON is correct")
    @pytest.mark.parametrize("name, expected_value, error_message", PET.expected_pet_names_keys_negative)
    def test_update_pet_info_with_invalid_id_json_values_negative(self, pet_data_set, update_headers,
                                                                  name, expected_value, error_message):
        """
        This test case validates that updating pet information with invalid id returns the expected response.
        :param for name: "code", "type", "message" (keys)
        :param for expected_value: 404, "unknown", pet_id=-1
        :param for error_message: "Response JSON doesn't have key {name}"
        """
        pet_id = -1
        response = MyRequests.post(
            self.link.PET + f"/{pet_id}",
            pet_data_set,
            headers=update_headers)
        Assertions.assert_json_value_by_name(response, name, expected_value, error_message)

    @allure.title("Update pet with invalid method > Status code is 405")
    def test_update_pet_info_status_code_405(self, pet_data_set, headers, update_headers, ):
        """ This test case ensures status code is 405 for updating a pet's info with invalid method."""
        # Creating pet
        response = MyRequests.post(
            self.link.PET,
            pet_data_set,
            headers=headers
        )
        actual_pet_id = int(response.json()["id"])
        # Sending the PUT (wrong method) instead of POST to update pet's info
        pet_data_set["name"] = PET.pet["pet_name"]
        pet_data_set["status"] = PET.pet["pet_status"]
        response = MyRequests.put(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set,
            headers=update_headers)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_405)
