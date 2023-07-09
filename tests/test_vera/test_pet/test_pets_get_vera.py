import allure
import pytest

from src.assertions import Assertions
from src.http_methods import MyRequests
from data.data_pet import get_pet_by_status
from data.status_code import StatusCode
from data.urls import PetUrls
from tests.test_vera.conf import headers, pet_data_set
from tests.test_vera.data.data_pets import ExpectedPetsResult as PET


@allure.epic('GET: get pets from the store')
class TestPet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Find pets by status > Status code is 200")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_get_pet_by_status_has_status_code_200(self, status):
        """
        This test checks availability of pets by status
        and checks the status code of the response
        :param for status: "available", "pending",  "sold"
        """
        response = MyRequests.get(
            self.link.BY_STATUS,
            status
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Find pets by status > Expected number of pets for each status")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_pets_count_by_status(self, status):
        """
        The test checks if the response contains the expected number of pets for each status
        :param for status: "available", "pending",  "sold"
        """
        response = MyRequests.get(
            self.link.BY_STATUS,
            data=status
        )
        data = response.json()
        assert isinstance(data, list)
        assert all(pet['status'] == status['status'] for pet in data)

    @allure.title("Find pets by status > Response content type is JSON")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_get_pet_by_status_response_content_type(self, status):
        """ The test checks if the response content type is JSON """
        response = MyRequests.get(
            self.link.BY_STATUS,
            data=status
        )
        Assertions.assert_response_has_be_json(response)

    @allure.title("Find pets by status > Response headers contain the necessary fields")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_get_pet_by_status_response_headers(self, status):
        """ The test checks if the response headers contain the necessary fields"""
        response = MyRequests.get(
            self.link.BY_STATUS,
            data=status
        )
        for header, value in response.headers.items():
            print(f"{status} - {header}: {value}")
            if header in PET.get_pet_by_status_headers:
                assert header in response.headers, f"Expected header '{header}' not found"
                assert value == PET.get_pet_by_status_headers[
                    header], f"Expected value '{PET.get_pet_by_status_headers[header]}' for header '{header}'"

    @allure.title("Find pets by invalid status > Response content is empty")
    def test_get_pet_by_invalid_status(self):
        """ The test checks if the response content type is JSON """
        data = {
            "status": "invalid_status"
        }
        response = MyRequests.get(
            self.link.BY_STATUS,
            data=data
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        Assertions.assert_json_has_not_keys(response, PET.expected_pet_keys)
        assert response.json() == []

    @allure.title("Get a pet by ID > Status code is 200")
    def test_get_pet_by_id_status_code(self, pet_data_set):
        """This test to get pet info by ID and ensures status code is 200"""
        # creating a pet
        response = MyRequests.post(
            self.link.PET,
            data=pet_data_set,
        )
        pet_id = response.json()['id']
        # getting status code for the response
        response = MyRequests.get(
            self.link.PET + f"/{pet_id}",
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Get a pet by non-existing ID > Status code is 404")
    def test_get_pet_by_non_existing_id_status_code_404(self, pet_data_set):
        """This test to get pet info by non-existing ID and ensures status code is 404"""
        pet_id = -1
        response = MyRequests.get(
            self.link.PET + f"/{pet_id}",
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)

    @allure.title("Get a pet by non-existing ID > Error message in the response")
    @pytest.mark.parametrize("name, expected_value, error_message", PET.expected_non_exist_pet_names_keys)
    def test_get_pet_by_non_existing_id_error_message(self, pet_data_set, name, expected_value, error_message):
        """
        This test verifies the response for retrieving pet information by non-existing ID
        and validates error message in the response.
        """
        pet_id = -1
        response = MyRequests.get(
            self.link.PET + f"/{pet_id}",
        )
        Assertions.assert_json_value_by_name(response, name, expected_value, error_message)

    @allure.title("Get a pet by ID > Status code is 404 after deleting the pet")
    def test_get_pet_by_id_after_deleting_status_404(self, pet_data_set):
        pet_data_set["pet_id"] = PET.pet["pet_id"]
        # Creating a pet
        response = MyRequests.post(
            self.link.PET,
            data=pet_data_set
        )
        # Deleting the pet and checking the status code is 200
        actual_pet_id = int(response.json()["id"])
        response = MyRequests.delete(
            self.link.PET + f"/{actual_pet_id}",
            data=pet_data_set
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)
        response = MyRequests.get(
            self.link.PET + f"/{actual_pet_id}",
        )
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)
