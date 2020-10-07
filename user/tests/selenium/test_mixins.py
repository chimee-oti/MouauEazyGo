from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase
from django.urls import reverse
import pytest
from user.tests.factories import UserFactory
from user.tests.selenium.common import Common
import time


@pytest.mark.skip
class TestUpdateViewMixin(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path="E:\PC PROGRAMS\chromedriver_win32/chromedriver")
        self.user = UserFactory()


    def test_form_updated(self):
        driver = self.driver
        registered_user = Common.Register(driver=driver, user=self.user)
        logged_user = Common.Login(driver=driver, user=registered_user)
        time.sleep(10)
        driver.get("http://localhost:8080" + reverse('profile_update'))
        time.sleep(30)
        driver.close()
        self.assertIn("MouauEasyGo", driver.title)
