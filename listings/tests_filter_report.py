import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

login_button_path = '//*[@id="login_btn"]'
username_field_path = '//*[@id="id_username"]'
password_field_path = '//*[@id="id_password"]'
submit_button_path = '//*[@id="submit_btn"]'
error_msg_path = '//*[@id="error_msg"]'
report_button_path = "//button[contains(., 'Filter report')]"

def test_admin_login(driver):
    try:
        login_button = driver.find_element(By.XPATH, login_button_path)


        login_button.click()

        username_field = driver.find_element(By.XPATH, username_field_path)
        username_field.click()
        username_field.send_keys("admin")

        password_field = driver.find_element(By.XPATH, password_field_path)
        password_field.send_keys("admin")
        time.sleep(4)

        submit_button = driver.find_element(By.XPATH, submit_button_path)
        submit_button.click()
        time.sleep(4)

        click_button = driver.find_element(By.XPATH, report_button_path)
        click_button.click()
        time.sleep(4)
        assert True

    except Exception as e:
        print('Something went wrong')
        driver.close()


class HostTest(LiveServerTestCase):
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8000/')
    time.sleep(5)
    test_admin_login(driver)
