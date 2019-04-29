from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException

import os
import sys
import platform
import time


ADDRESS = 'http://127.0.0.1:8000/'
driver = None

# Setup the headless browser with Gecko for Firefox and open reddit's login page
# Note: firefox (gecko) driver must be in system PATH for this to work
def setup():
    global driver
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Visit the webpage.
    driver.get("https://reddit.com/login")


# Returns False if login failed with supplied credentials, True otherwise
def do_login(**credentials):
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

    # Is the 2FA page showing up?
    while True:
        time.sleep(0.3)
        length_error = len(driver.find_elements_by_class_name('m-error'))
        length_twofa = len(driver.find_elements_by_class_name('mode-2fa'))
        if length_error > 0:
            return False # creds were not correct
        if length_twofa > 0:
            return True # creds were valid
    

def go():
    setup()
    cred_correct = do_login(Username="2fabusters-fakeee", Password="attackatdawn", Code="000000")
    print(cred_correct)
go()