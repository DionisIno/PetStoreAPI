from data.data_pet import pet_id

BASE_URL = "https://petstore.swagger.io/v2"


class PetUrls:
    BY_STATUS = "/pet/findByStatus"
    PET = "/pet"
    PET_ID = f"/pet/{pet_id}"


class UserUrls:
    CREATE_USER = "/user"
