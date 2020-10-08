from selenium import webdriver
from user.tests.factories import UserFactory
from django.urls import reverse
import time


class Common(object):

    def Register(driver, user):
        driver.get("http://localhost:8080" + reverse('register'))
        time.sleep(2)
        
        email_field = driver.find_element_by_id("id_email")
        email_field.click()
        email_field.clear()
        email_field.send_keys(user.email)
        
        username_field = driver.find_element_by_id("id_username")
        username_field.click()
        username_field.clear()
        username_field.send_keys(user.username)
        
        firstname_field = driver.find_element_by_id("id_firstname")
        firstname_field.click()
        firstname_field.clear()
        firstname_field.send_keys(user.firstname)
        
        lastname_field = driver.find_element_by_id("id_lastname")
        lastname_field.click()
        lastname_field.clear()
        lastname_field.send_keys(user.lastname)
        
        password1_field = driver.find_element_by_id("id_password1")
        password1_field.click()
        password1_field.clear()
        password1_field.send_keys(user.password)
        
        password2_field = driver.find_element_by_id("id_password2")
        password2_field.click()
        password2_field.clear()
        password2_field.send_keys(user.password)
        
        date_of_birth_field = driver.find_element_by_id("id_date_of_birth")
        date_of_birth_field.click()
        date_of_birth_field.clear()
        date_of_birth_field.send_keys(str(user.profile.date_of_birth))
        
        image_field = driver.find_element_by_id("id_image")
        image_field.send_keys(
            r"C:\Users\Elisha\Pictures\Screenshots\Screenshot (16).png")
        
        driver.find_element_by_id("register").click()
        time.sleep(10)
        return user

    def Login(driver, user):
        driver.get("http://localhost:8080" + reverse('login'))
        
        username_field = driver.find_element_by_name("username")
        username_field.click()
        username_field.send_keys(user.username)
        
        password_field = driver.find_element_by_name("password")
        password_field.click()
        password_field.send_keys(user.password)
        
        submit_button = driver.find_element_by_id("login")
        submit_button.click()
        return user
