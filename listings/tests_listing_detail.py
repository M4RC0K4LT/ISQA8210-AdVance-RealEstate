import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

listing_path = "//button[contains(.,'Explore Properties')]"
contact_path = "//button[contains(.,'CLICK TO CONTACT AGENT TODAY!')]"

class tests_listing_detail(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tests_detail(self):
        driver = self.driver
        driver.maximize_window()
        driver.get('http://127.0.0.1:8000/')
        time.sleep(5)
        listing_button = driver.find_element(By.XPATH, listing_path)
        listing_button.click()
        time.sleep(4)
        driver.get('http://127.0.0.1:8000/listing/4')
        time.sleep(4)
        try:
            elem = driver.find_element(By.XPATH, contact_path)
            driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("error occured on listing detail test case")
            driver.close()


if __name__ == "__main__":
    unittest.main()