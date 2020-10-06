from selenium import webdriver
from user.tests.factories import UserFactory
from django.urls import reverse


class Common(object):
    def __init__(self, driver):
        self.driver = webdriver.Chrome(
            executable_path="E:\PC PROGRAMS\chromedriver_win32/chromedriver")
        self.user = UserFactory()

    def Register(self):
        driver = self.driver
        driver.get("http://localhost:8000" + reverse('register'))
        