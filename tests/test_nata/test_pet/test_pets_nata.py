from data.urls import PetUrls
from src.http_methods import MyRequests
from src.assertions import Assertions
from data.status_code import StatusCode


class TestPet:
    status_code = StatusCode
    link = PetUrls

    def test_get_pet_by_id(self):
        """This test as example. I'm going to improve it"""
        response = MyRequests.get(self.link.PET_ID)
        print('', response.url, response.text, sep='\n')
        Assertions.assert_code_status(response, self.status_code.STATUS_CODE_404)
