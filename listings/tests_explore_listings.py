import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

# Declare all the paths
explore_button_path = "/html/body/nav/div[2]/nav/div/ul/li[2]/a/button"
property_type_path = '//*[@id="id_property_type"]'
select_apart_path = '//*[@id="id_property_type"]/option[2]'
property_neigh_path = '//*[@id="id_property_neighborhood"]'
select_neigh_path = '//*[@id="id_property_neighborhood"]/option[2]'
property_price_range_path = '//*[@id="id_property_price_range"]'
select_price_path = '//*[@id="id_property_price_range"]/option[2]'
submit_button_path = '/html/body/div/form/input'


def test_explore_listings(driver):
    try:
        # click explore listings
        explore_button = driver.find_element(By.XPATH, explore_button_path)
        time.sleep(2)
        assert explore_button.is_displayed()
        explore_button.click()

        # click property type & select apartment from dropdown
        property_type = driver.find_element(By.XPATH, property_type_path)
        property_type.click()
        select_apart = driver.find_element(By.XPATH, select_apart_path)
        select_apart.click()

        # click property neighbourhood & select downtown from dropdown
        property_neigh = driver.find_element(By.XPATH, property_neigh_path)
        property_neigh.click()
        select_neigh = driver.find_element(By.XPATH, select_neigh_path)
        select_neigh.click()

        # click property price & select range from dropdown
        property_price_range = driver.find_element(By.XPATH, property_price_range_path)
        select_price = driver.find_element(By.XPATH, select_price_path)
        select_price.click()
        time.sleep(2)

        # click sumbit button & see the details page
        submit_button = driver.find_element(By.XPATH, submit_button_path)
        submit_button.click()
        time.sleep(5)

    except:
        print('Something went wrong on the explore listings test case')
        driver.close()


class HostTest(LiveServerTestCase):
    # Initialize the web_driver & get the url to open in chrome browser
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8000/')
    time.sleep(5)

    # call test case
    test_explore_listings(driver)
