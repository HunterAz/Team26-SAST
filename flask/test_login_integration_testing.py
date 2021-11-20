import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class test_login_credential(unittest.TestCase):

    def test_login_driver_class(self):
        def __init__(self):
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--incognito")
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            driver = webdriver.Chrome(r'flask/website/chromedriver/chromedriver.exe',chrome_options=options)
            driver.get("https://meok.sitict.net/")
            username = driver.find_element_by_id("username")
            username.click()
            username.send_keys('testuser')
            password = driver.find_element_by_id("password")
            password.click()
            password.send_keys('testuser')
            password.send_keys(Keys.ENTER)
            if driver.find_element_by_xpath('/html/body/div[1]/nav/div/ul/li[5]/a').is_displayed():
                if driver.find_element_by_xpath('/html/body/div[1]/nav/div/ul/li[5]/a').is_enabled():
                    if driver.find_element_by_class_name('verifyOTP').is_displayed():
                        if driver.find_element_by_class_name('verifyOTP').is_enabled():
                            driver.find_element_by_class_name('verifyOTP')
                            driver.quit()

if __name__ == '__main__':
    unittest.main()