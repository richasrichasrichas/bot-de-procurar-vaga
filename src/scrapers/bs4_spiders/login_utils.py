# src/scrapers/bs4_spiders/login_utils.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login_to_website(driver, username, password):
    driver.get('https://www.indeed.com')

    # Wait for the page to load
    time.sleep(2)

    # Locate the username and password fields and enter the credentials
    username_field = driver.find_element(By.NAME, 'username')  # Replace 'username' with the actual name attribute of the username field
    password_field = driver.find_element(By.NAME, 'password')  # Replace 'password' with the actual name attribute of the password field

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the form
    password_field.send_keys(Keys.RETURN)

    # Wait for the login process to complete
    time.sleep(5)