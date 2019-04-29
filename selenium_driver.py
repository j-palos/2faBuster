from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException

import os
import sys
import platform
import time

ADDRESS = 'http://127.0.0.1:8000/'


# Note: firefox (gecko) driver must be in system PATH for this to work
def do_login(**credentials):
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # Visit the webpage.
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
    error_found = False
    twoauth_found = False
    while not error_found and not twoauth_found:
        time.sleep(0.3)
        length_error = len(driver.find_elements_by_class_name('m-error'))
        print("length_error" + str(length_error))
        length_twofa = len(driver.find_elements_by_class_name('mode-2fa'))
        print("length_twofa" + str(length_twofa))
        if length_error > 0:
            error_found = True
        if length_twofa > 0:
            twoauth_found = True


    if error_found:
        print("an error was found")
    elif twoauth_found:
        print("got to twoauth field")
    # try:
    #     driver.find_element_by_class_name('m-error')
    #     print("! ! ERROR ! !")
    # except NoSuchElementException:
    #     print("no error icon after 3 seconds")
    # print(submit_btn.get_attribute("innerHTML"))

    

def go():
    do_login(Username="2fabusters", Password="attackatdawn", Code="000000")

go()