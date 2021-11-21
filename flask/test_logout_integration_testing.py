import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class test_logout_credential(unittest.TestCase):

    def test_logout_driver_class(self):
        def __init__(self):
            driver_path = r'flask/website/chromedriver/chromedriver.exe'
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--incognito")
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            self.driver = webdriver.Chrome(driver_path, chrome_options=options)
            self.driver.get("https://meok.sitict.net/")
            username = self.driver.find_element_by_id("username")
            username.click()
            username.send_keys('testuser')
            password = self.driver.find_element_by_id("password")
            password.click()
            password.send_keys('testuser')
            password.send_keys(Keys.ENTER)
            if self.driver.find_element_by_xpath('/html/body/div[1]/nav/div/ul/li[5]/a').is_displayed():
                if self.driver.find_element_by_xpath('/html/body/div[1]/nav/div/ul/li[5]/a').is_enabled():
                    logout = self.driver.find_element_by_xpath('/html/body/div[1]/nav/div/ul/li[5]/a')
                    logout.click()
                    self.driver.quit()
if __name__ == '__main__':
    unittest.main()