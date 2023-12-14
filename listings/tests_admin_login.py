import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

# Declare all the paths
login_button_path = '//*[@id="login_btn"]'
username_field_path = '//*[@id="id_username"]'
password_field_path = '//*[@id="id_password"]'
submit_button_path = '//*[@id="submit_btn"]'
error_msg_path = '//*[@id="error_msg"]'


def test_admin_login(driver):
    try:
        # click explore listings
        login_button = driver.find_element(By.XPATH, login_button_path)

        assert login_button.is_displayed()
        login_button.click()

        # click property type & select apartment from dropdown
        username_field = driver.find_element(By.XPATH, username_field_path)
        username_field.click()
        username_field.send_keys("username")
        
        password_field = driver.find_element(By.XPATH, password_field_path)
        password_field.send_keys("password")
        time.sleep(4)
        
        submit_button = driver.find_element(By.XPATH, submit_button_path)
        submit_button.click()
        time.sleep(4)
        
        try:
            driver.find_element(By.XPATH, error_msg_path)
        except:
            print("Something went wrong on the admin login test case")
            driver.close()
            return
        
    except Exception as e:
        print("Something went wrong on the admin login test case")
        driver.close()


class HostTest(LiveServerTestCase):
    # Initialize the web_driver & get the url to open in chrome browser
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8000/')
    time.sleep(5)

    # call test case
    test_admin_login(driver)
