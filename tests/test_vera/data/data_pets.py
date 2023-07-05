import random
from generator.generator import generated_pet

class ExpectedPetsResult:
    expected_pet_keys = ['id', 'category', 'name', 'photoUrls', 'tags', 'status']

    pet_data = next(generated_pet())
    pet = {
        "pet_id": str(92233720169000) + str(random.randint(10000, 99999)),
        "pet_name": pet_data.name,
        "photo_urls": pet_data.photoUrls,
        "pet_status": pet_data.status,
        "pet_breed": pet_data.breed,
    }

    expected_pet_names_keys_positive = [
        ("code", 200, "Response JSON doesn't have key 'code'"),
        ("type", "unknown", "Response JSON doesn't have key 'type'"),
        ("message", pet['pet_id'], "Response JSON doesn't have key 'message'")
        ]

    expected_pet_names_keys_negative = [
        ("code", 404, "Response JSON doesn't have key 'code'"),
        ("type", "unknown", "Response JSON doesn't have key 'type'"),
        ("message", "not found", "Response JSON doesn't have key 'message'")
    ]

    get_pet_by_status_headers = ['access-control-allow-headers', 'access-control-allow-methods',
                                 'access-control-allow-origin',
                                 'content-type', 'content-type', 'date', 'server']
