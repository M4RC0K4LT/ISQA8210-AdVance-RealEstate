import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

# Declare all the paths
featured_listing_path = '//*[@id="featured_listing_link"]'
listing_title_path = '//*[@id="listing_title_div"]'


def test_featured_listing(driver):
    try:
        # click explore listings
        featured_listing = driver.find_element(By.XPATH, featured_listing_path)

        assert featured_listing.is_displayed()
        featured_listing.click()

        
        try:
            driver.find_element(By.XPATH, listing_title_path)
        except:
            print('Something went wrong on the featured property test case')
            driver.close()
            return
        
    except Exception as e:
        print('Something went wrong on the featured property test case')
        driver.close()


class HostTest(LiveServerTestCase):
    # Initialize the web_driver & get the url to open in chrome browser
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8000/')
    time.sleep(5)

    # call test case
    test_featured_listing(driver)
