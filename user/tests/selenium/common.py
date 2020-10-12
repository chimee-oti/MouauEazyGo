from selenium import webdriver
from user.tests.factories import UserFactory
from django.urls import reverse
import time
from faker import Faker
from user.models import User


class Common(object):

    def Register(driver):
        fake = Faker()
        driver.get("http://localhost:8080" + reverse('account_signup'))
        time.sleep(2)
        
        email_field = driver.find_element_by_id("id_email")
        email_field.click()
        email_field.clear()
        email = fake.email()
        email_field.send_keys(email)
        
        username_field = driver.find_element_by_id("id_username")
        username_field.click()
        username_field.clear()
        username_field.send_keys(fake.user_name())
        
        firstname_field = driver.find_element_by_id("id_firstname")
        firstname_field.click()
        firstname_field.clear()
        firstname_field.send_keys(fake.first_name())
        
        lastname_field = driver.find_element_by_id("id_lastname")
        lastname_field.click()
        lastname_field.clear()
        lastname_field.send_keys(fake.last_name())
        
        password1_field = driver.find_element_by_id("id_password1")
        password1_field.click()
        password1_field.clear()
        password = fake.password()
        password1_field.send_keys(password)
        
        password2_field = driver.find_element_by_id("id_password2")
        password2_field.click()
        password2_field.clear()
        password2_field.send_keys(password)
        
        date_of_birth_field = driver.find_element_by_id("id_date_of_birth")
        date_of_birth_field.click()
        date_of_birth_field.clear()
        date_of_birth_field.send_keys(str(fake.date_of_birth()))
        
        image_field = driver.find_element_by_id("id_image")
        image_field.send_keys(
            r"E:\Picture\Happy birthday Esther ❤️ 20200120_105048.jpg")
        
        driver.find_element_by_id("register").click()
        all_users = User.objects.all()
        user = all_users.get(email=email)
        return user

    def Login(driver, user):
        driver.get("http://localhost:8080" + reverse('account_login'))
        
        username_field = driver.find_element_by_name("username")
        username_field.click()
        username_field.send_keys(user.username)
        
        password_field = driver.find_element_by_name("password")
        password_field.click()
        password_field.send_keys(user.password)
        
        submit_button = driver.find_element_by_id("login")
        submit_button.click()
        return user
