import json
import os

import allure


class BasePage:
    @allure.step("Create json file with data")
    def write(self, data, name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = f"""{name}.json"""
        file_path = os.path.join(current_dir, "..", file_name)
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @allure.step("Read json file")
    def read(self, name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = f"""{name}.json"""
        file_path = os.path.join(current_dir, "..", file_name)
        with open(file_path, 'r', encoding="utf-8") as file:
            file_data = json.load(file)
        return file_data

    def create_pet(self):
        data = {
          "id": 0,
          "category": {
            "id": 0,
            "name": "string"
          },
          "name": "doggie",
          "photoUrls": [
            "string"
          ],
          "tags": [
            {
              "id": 0,
              "name": "string"
            }
          ],
          "status": "available"
        }