from selenium import webdriver
from user.tests.factories import UserFactory
from django.urls import reverse
import time


class Common(object):

    def Register(driver, user):
        driver.get("http://localhost:8080" + reverse('register'))
        time.sleep(2)
        
        driver.find_element_by_id("id_email").click()
        driver.find_element_by_id("id_email").clear()
        driver.find_element_by_id("id_email").send_keys(user.email)
        
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(user.username)
        
        driver.find_element_by_id("id_firstname").click()
        driver.find_element_by_id("id_firstname").clear()
        driver.find_element_by_id("id_firstname").send_keys(user.firstname)
        
        driver.find_element_by_id("id_lastname").click()
        driver.find_element_by_id("id_lastname").clear()
        driver.find_element_by_id("id_lastname").send_keys(user.lastname)
        
        driver.find_element_by_id("id_password1").click()
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys(user.password)
        
        driver.find_element_by_id("id_password2").click()
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys(user.password)
        
        driver.find_element_by_id("id_date_of_birth").click()
        driver.find_element_by_id("id_date_of_birth").clear()
        driver.find_element_by_id("id_date_of_birth").send_keys(str(user.profile.date_of_birth))
        
        driver.find_element_by_id("id_image").send_keys(r"C:\Users\Elisha\Pictures\Screenshots\Screenshot (16).png")
        
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
