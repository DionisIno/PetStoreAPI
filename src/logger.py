import datetime
import os
from requests import Response


class Logger:
    file_name = f"""log_{str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))}.log"""

    current_dir = os.path.dirname(os.path.abspath(__file__))

    project_dir = os.path.dirname(current_dir)

    # Формирование пути к директории logs
    logs_dir = os.path.join(project_dir, 'logs')

    # Проверка существования директории logs
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Формирование пути к файлу логов
    log_file = os.path.join(logs_dir, file_name)

    @classmethod
    def _write_log_to_file(cls, data: str):

        with open(cls.log_file, 'a', encoding="utf=8") as logger_file:
            logger_file.write(data)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        test_name = os.environ.get("PYTEST_CURRENT_TEST")

        data_to_add = f"\n{'-'*120}\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += f"\n{'-'*120}\n"

        cls._write_log_to_file(data_to_add)
