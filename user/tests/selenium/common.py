from selenium import webdriver
from user.tests.factories import UserFactory
from django.urls import reverse


class Common(object):
    def __init__(self):
        self.driver = webdriver.Chrome(
            executable_path="E:\PC PROGRAMS\chromedriver_win32/chromedriver")
        self.user = UserFactory()

    def Register(self):
        driver = self.driver
        driver.get("http://localhost:8000" + reverse('register'))
        email_field = driver.find_element_by_name("email")
        email_field.clear()
        email_field.send_keys(self.user.email)
        username_field = driver.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys(self.user.username)
        firstname_field = driver.find_element_by_name("firstname")
        firstname_field.clear()
        firstname_field.send_keys(self.user.firstname)
        lastname_field = driver.find_element_by_name("lastname")
        lastname_field.clear()
        lastname_field.send_keys(self.user.lastname)  
        password1_field = driver.find_element_by_name("password1")
        password1_field.clear()
        password1_field.send_keys(self.user.password)
        password2_field = driver.find_element_by_name("password2")
        password2_field.clear()
        password2_field.send_keys(self.user.password)
        date_of_birth_field = driver.find_element_by_name("birth_of_birth")
        date_of_birth_field.clear()
        date_of_birth_field.send_keys(self.user.profile.date_of_birth)
        image_field = driver.find_element_by_name("image")
        image_field.clear()
        image_field.send_keys(self.user.profile.image)
        submit_button = driver.find_element_by_id("register")
        submit_button.click()
        return self.user
    
    
    def Login(self):    
        driver = self.driver
        driver.get("http://localhost:8080" + reverse('login'))
        username_field = driver.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys(self.user.username)
        password_field = driver.find_element_by_name("password")
        password_field.clear()
        password_field.send_keys(self.user.password)
        submit_button = driver.find_element_by_id("login")
        submit_button.click()
        return self.user