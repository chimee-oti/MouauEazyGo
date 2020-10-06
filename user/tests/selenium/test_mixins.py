from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase
from django.urls import reverse
import pytest
from user.tests.factories import UserFactory
from user.tests.selenium.common import RegisterAndLogin


@pytest.mark.webtest
class TestUpdateViewMixin(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path="E:\PC PROGRAMS\chromedriver_win32/chromedriver")
        self.user = UserFactory()

    def test_form_updated(self):
        driver = self.driver
        driver.get("http://localhost:8080" + reverse('profile_update'))
        username_field = driver.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys(self.user.username)
        password_field = driver.find_element_by_name("password")
        password_field.clear()
        password_field.send_keys(self.user.password)

        submit_button = driver.find_element_by_id("login")
        submit_button.click()
        driver.save_screenshot("E:/pictures/screen.png")

        driver.implicitly_wait(100)
        driver.close()
        self.assertIn("MouauEasyGo", driver.title)
