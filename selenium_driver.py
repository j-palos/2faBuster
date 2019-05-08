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
import uuid

# constants
TITLE_TO_MATCH = 'reddit: the front page of the internet'
INVALID_CREDS = -1
SUCCESS_NO_TWOAUTH = 0
SUCCESS_TWOAUTH = 1

# Setup the headless browser with Gecko for Firefox and open reddit's login page
# Note: firefox (gecko) driver must be in system PATH for this to work
def setup():
    options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)

    # Visit the webpage.
    driver.get('https://reddit.com/login')

    return driver


# Returns False if login failed with supplied credentials, True otherwise
def do_login(driver, **credentials):
    # Send credentials
    user_field = driver.find_element_by_id('loginUsername')
    pass_field = driver.find_element_by_id('loginPassword')
    user_field.clear()
    user_field.send_keys(credentials['Username'])
    pass_field.clear()
    pass_field.send_keys(credentials['Password'])
    submit_btn = driver.find_element_by_class_name('AnimatedForm__submitButton')
    submit_btn.click()

    # Which page is showing up?
    while True:
        length_error = len(driver.find_elements_by_class_name('m-error'))
        length_twofa = len(driver.find_elements_by_class_name('mode-2fa'))
        length_notwofa = len(driver.find_elements_by_class_name('m-success'))
        if length_error > 0:
            return INVALID_CREDS # creds were not correct
        if length_twofa > 0:
            return SUCCESS_TWOAUTH # creds were valid and auth page presented
        if length_notwofa > 0:
            print('logged in, no twoauth')
            return SUCCESS_NO_TWOAUTH # successfully logged in without two auth
        

# returns -1 if login failed due to invalid auth or other error
# 0 upon login success only
# pre: make sure code is exactly 6 digits when calling this function
def do_twoauth(driver, code):
    # throw an error if the 2fa field cannot be found
    otp_field = None
    print("attempting 2auth...")
    try:
        otp_field = driver.find_element_by_id('loginOtp')
    except NoSuchElementException:
        print('Fatal error: twoauth field not found.')
        return False
    
    otp_field.clear()
    otp_field.send_keys(code)
    otp_field.send_keys(Keys.RETURN)

    while True:
        error_len = len(driver.find_elements_by_class_name('m-error'))
        auth_len = len(driver.find_elements_by_class_name('m-success'))
        if error_len > 0:
            print('error found')
            return False
        if auth_len > 0:
            try:
                time.sleep(0.5)
                title_reddit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'title')))
                if title_reddit.get_property('innerHTML') == TITLE_TO_MATCH:
                    print(TITLE_TO_MATCH)
                    print('Login was successfully completed')
                    return True
            except TimeoutException:
                print('Loading took too much time!')
                return False


# Change the password and disable their 2fa! New password will be returned; False if error
def do_password_change(driver, old_password):
    # password change to random uuid.hex format
    print("changing password")
    driver.get('https://www.reddit.com/prefs/update')
    temp_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'emailverification-edit')))
    temp_button.send_keys(Keys.TAB)
    current_password_field = driver.switch_to.active_element
    current_password_field.send_keys(old_password)
    new_password = str(uuid.uuid4().hex)
    driver.find_element_by_name('newpass').send_keys(new_password)
    driver.find_element_by_name('verpass').send_keys(new_password)
    deauth_checkbox = driver.find_element_by_id('invalidate_oauth')
    deauth_checkbox.click()
    deauth_checkbox.send_keys(Keys.TAB)
    save_button = driver.switch_to.active_element
    save_button.click()
    time.sleep(1)
    print('password changed')
    print('new password: ' + new_password)

    # disable 2fa
    disable_tfa_list = driver.find_elements_by_id('tfa-enable-col-second-variant')
    print(disable_tfa_list)
    if len(disable_tfa_list) > 0 and disable_tfa_list[0].is_displayed():
        print('disabling twofa')
        disable_tfa_list[0].click()
        while True:
            time.sleep(0.5)
            if len(driver.find_elements_by_class_name('modal-open')) > 0:
                break
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(new_password)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(Keys.RETURN)

    return new_password
    

def go(user, pswd, token):
    driver = setup()
    cred_status = do_login(driver, Username=user,
                           Password=pswd)
    twoauth_correct = False
    if cred_status == SUCCESS_TWOAUTH:
        print('login good; trying twoauth')
        twoauth_correct = do_twoauth(driver, token)
        if twoauth_correct:
            do_password_change(driver, pswd)
    elif cred_status == SUCCESS_NO_TWOAUTH:
        print('no twoauth, we are in. Time to change password')
        do_password_change(driver, pwsd)

if __name__ == '__main__':
    go(sys.argv[1], sys.argv[2], sys.argv[3])

