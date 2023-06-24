import random
import uuid
from faker import Faker
from data.pet_breed import get_breed
from data.data import Pet

faker = Faker()


def generated_pet():
    yield Pet(
        id_number=random.randint(1, 10000),
        name=faker.first_name(),
        photoUrls=generate_random_photo_url(),
        status=random.choice(["available", "pending", "sold"]),
        breed=get_breed()

    )


def generate_random_photo_url():
    base_url = "https://example.com/images/"
    image_name = str(uuid.uuid4())
    full_image_url = f"""{base_url}{image_name}.jpg"""
    return full_image_url

