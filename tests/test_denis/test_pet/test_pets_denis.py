import allure
import pytest
from src.assertions import Assertions
from src.http_methods import MyRequests
from data.data_pet import get_pet_by_status
from data.status_code import StatusCode
from data.urls import PetUrls


class TestPet:
    status_code = StatusCode()
    link = PetUrls

    @allure.title("Find pets by status and get status code of the response")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_get_pet_by_status_has_status_code_200(self, status):
        """
        This test will check the presence of pets by status and check the status code of the response
        :param status: "available", "pending",  "sold"
        """
        response = MyRequests.get(self.link.BY_STATUS, status)
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_200)

    @allure.title("Find pets by status and make sure the response is json")
    @pytest.mark.parametrize("status", get_pet_by_status)
    def test_get_pet_by_status_has_json_response(self, status):
        """
        This test checks that the response came in json format
        :param status: "available", "pending",  "sold"
        """
        response = MyRequests.get(self.link.BY_STATUS, status)
        Assertions.assert_response_has_be_json(response)
