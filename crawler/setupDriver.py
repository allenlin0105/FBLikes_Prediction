import time

from dotenv import dotenv_values
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def setupDriver() -> WebDriver:
    env = dotenv_values(".env")

    url = "https://www.facebook.com"
    email = env['EMAIL']
    password = env['PASSWORD']

    chrome_options = ChromeOptions()
    prefs = {
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get(url)

    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    time.sleep(5) 
    
    return driver
