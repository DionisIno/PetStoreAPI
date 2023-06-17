from faker import Faker
import random

get_pet_by_status = [{"status": "available"},
                     {"status": "pending"},
                     {"status": "sold"}
                     ]

fake = Faker()
pet_id = random.randint(1, 2000)
name = fake.first_name()
weekday = fake.day_of_week()

post_add_new_pet = {
    "id": pet_id,
    "category": {
        "id": 0,
        "name": "Dog"
    },
    "name": name,
    "photoUrls": [
        "string"
    ],
    "tags": [
        {
            "id": 0,
            "name": weekday
        }
    ],
    "status": "available"
}
