from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import os
import sys
import platform
import time


ADDRESS = 'http://127.0.0.1:8000/'
TITLE_TO_MATCH = "reddit: the front page of the internet"
driver = None

# Setup the headless browser with Gecko for Firefox and open reddit's login page
# Note: firefox (gecko) driver must be in system PATH for this to work
def setup():
    global driver
    options = webdriver.FirefoxOptions()
    #options.add_argument("--headless")
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

    # Is the 2FA page showing up?
    while True:
        length_error = len(driver.find_elements_by_class_name('m-error'))
        length_twofa = len(driver.find_elements_by_class_name('mode-2fa'))
        if length_error > 0:
            return False # creds were not correct
        if length_twofa > 0:
            return True # creds were valid


# returns -1 if login failed due to invalid auth or other error
# 0 upon login success only
# pre: make sure code is exactly 6 digits when calling this function
def do_twoauth(code):
    # throw an error if the 2fa field cannot be found
    otp_field = None
    try:
        otp_field = driver.find_element_by_id("loginOtp")
    except NoSuchElementException:
        print("Fatal error: twoauth field not found.")
        return -1
    
    otp_field.clear()
    otp_field.send_keys(code)
    otp_field.send_keys(Keys.RETURN)

    while True:
        error_len = len(driver.find_elements_by_class_name("m-error"))
        auth_len = len(driver.find_elements_by_class_name("m-success"))
        if error_len > 0:
            print("error found")
            return -1
        if auth_len > 0:
            try:
                title_reddit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'title')))
                if title_reddit.get_property("innerHTML") == TITLE_TO_MATCH:
                    print(TITLE_TO_MATCH)
                    print("Page is ready!")
                    return True
            except TimeoutException:
                print("Loading took too much time!")
                return False
        

def go():
    setup()
    cred_correct = do_login(Username="2fabusters", Password="attackatdawn")
    twoauth_corrent = False
    if cred_correct:
        twoauth_corrent = do_twoauth("000000")
    if twoauth_corrent:
        pass

if __name__ == '__main__':
    go()

