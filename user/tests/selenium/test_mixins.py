from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase
from django.urls import reverse
import pytest
from user.tests.factories import UserFactory
from user.tests.selenium.common import Common


@pytest.mark.skip
class TestUpdateViewMixin(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path="E:\PC PROGRAMS\chromedriver_win32/chromedriver")
        

    def test_form_updated(self):
        driver = self.driver
        common.Register
        self.user = common.Login
        driver.get("http://localhost:8080" + reverse('profile_update'))
       
        driver.save_screenshot("E:/pictures/screen.png")

        driver.implicitly_wait(100)
        driver.close()
        self.assertIn("MouauEasyGo", driver.title)
