from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import os
import sys
import platform
import time

ADDRESS = 'http://127.0.0.1:8000/'


# Note: firefox (gecko) driver must be in PATH for this to work
# htmlfile, **credentials
def do_login(htmlfile, **credentials):
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Visit this webpage.
    driver.get("https://reddit.com/login")

    # Send credentials
    user_field = driver.find_element_by_id('loginUsername')
    pass_field = driver.find_element_by_id('loginPassword')
    user_field.clear()
    user_field.send_keys(credentials['Username'])
    pass_field.clear()
    pass_field.send_keys(credentials['Password'])
    submit_btn = driver.find_element_by_class_name("AnimatedForm__submitButton")
    submit_btn.click()
    time.sleep(3)

    # Was the login successful? If so, is the 2FA page showing up?
    print(submit_btn.get_attribute("innerHTML"))

    

def go():
    # do_login("twofabuster.html", Username="pepe", Password="password")
    # do_login("authtoken.html", Password=1234) 
    do_login("login-orig.html", Username="2fabusters", Password="attackatdawn")

go()