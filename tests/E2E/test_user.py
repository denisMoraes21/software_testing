import unittest
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class TestUsersE2E(unittest.TestCase):

    def setUp(self):
        self.BASE_URL = "http://127.0.0.1:5000"
        self.PREFIX_ENDPOINT = "/users"
        self.CREATE_USER_ENDPOINT = f"{self.PREFIX_ENDPOINT}/create"
        self.DELETE_USER_ENDPOINT = f"{self.PREFIX_ENDPOINT}/delete"
        self.REGISTER_PAGE_ENDPOINT = f"{self.PREFIX_ENDPOINT}/register"
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

    def test_register_user(self):
        self.driver.get(f"{self.BASE_URL}{self.REGISTER_PAGE_ENDPOINT}")
        # time.sleep(2)

        username = self.driver.find_element(By.ID, "create-name")

        username.send_keys("Denis")

        # time.sleep(2)

        submit = self.driver.find_element(By.ID, "button-create")
        # time.sleep(2)

        submit.click()

        wait = WebDriverWait(self.driver, 10)

        alert = wait.until(
            EC.alert_is_present()
        )
        # time.sleep(2)

        self.assertEqual(
            alert.text,
            "Usuário criado com sucesso!"
        )

        _body = {
            "id": 1
        }

        requests.post(
            f"{self.BASE_URL}{self.DELETE_USER_ENDPOINT}",
            json=_body
        )

    def test_delete_user(self):
        _body = {
            "name": "Denis"
        }

        requests.post(
            f"{self.BASE_URL}{self.CREATE_USER_ENDPOINT}",
            json=_body
        )

        self.driver.get(f"{self.BASE_URL}{self.REGISTER_PAGE_ENDPOINT}")
        # time.sleep(2)

        username = self.driver.find_element(By.ID, "delete-id")

        username.send_keys(1)

        # time.sleep(2)

        submit = self.driver.find_element(By.ID, "button-delete")
        # time.sleep(2)

        submit.click()

        wait = WebDriverWait(self.driver, 10)

        alert = wait.until(
            EC.alert_is_present()
        )
        # time.sleep(2)

        self.assertEqual(
            alert.text,
            "Usuário deletado com sucesso!"
        )

        _body = {
            "id": 1
        }

        requests.post(
            f"{self.BASE_URL}{self.DELETE_USER_ENDPOINT}",
            json=_body
        )

    def tearDown(self):
        self.driver.quit()
