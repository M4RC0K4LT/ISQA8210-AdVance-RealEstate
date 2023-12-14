import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

# Declare all the paths
about_us_path = '//*[@id="aboutus_nav"]'
contact_button_path = '//*[@id="contact_madison_btn"]'
contact_submit_path = '//*[@id="contact_submit_btn"]'


def test_featured_listing(driver):
    try:
        # click explore listings
        about_us_nav = driver.find_element(By.XPATH, about_us_path)

        assert about_us_nav.is_displayed()
        about_us_nav.click()
        time.sleep(2)
        
        # click property type & select apartment from dropdown
        contanct_button = driver.find_element(By.XPATH, contact_button_path)
        contanct_button.click()        
        
        try:
            driver.find_element(By.XPATH, contact_submit_path)
        except:
            print('Something went wrong on the contact form test case')
            driver.close()
            return
        
    except Exception as e:
        print('Something went wrong on the contact form test case')
        driver.close()


class HostTest(LiveServerTestCase):
    # Initialize the web_driver & get the url to open in chrome browser
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8000/')
    time.sleep(5)

    # call test case
    test_featured_listing(driver)
