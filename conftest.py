import os
import shutil
import allure
import pytest


@allure.description("Function to clear the contents of the logs folder. Return: empty log folder")
@allure.step("Deleting all contents of the logs folder")
def clear_logs_directory():

    with allure.step("Getting the absolute path to the current file"):
        current_dir = os.path.dirname(os.path.abspath(__file__))

    with allure.step("Forming the path to the logs folder"):
        logs_dir = os.path.join(current_dir, 'logs')

    with allure.step("Checking if the logs folder exists"):
        if os.path.exists(logs_dir):
            # Deleting all content in the logs folder
            shutil.rmtree(logs_dir)

            # Create an empty logs folder
            os.makedirs(logs_dir)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Calling a function to clear the contents of the logs folder before starting a session
    """
    clear_logs_directory()
