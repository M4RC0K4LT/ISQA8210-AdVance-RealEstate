import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

omaha_page = "//button[contains(., 'Explore Omaha')]"
explore = "//h2[contains(., 'Explore Omaha like never before')]"


def test_explore_omaha(driver):
    try:

        button = driver.find_element(By.XPATH, omaha_page)
        button.click()
        time.sleep(4)
        driver.find_elemet(By.XPATH, explore)
        assert True

    except Exception as e:
        print('Something went wrong')
        driver.close()


class Test(LiveServerTestCase):
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8000/')
    time.sleep(5)
    test_explore_omaha(driver)
