from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ADDRESS = 'http://127.0.0.1:8000/'

# Note: firefox (gecko) driver must be in PATH for this to work
def do_login(htmlfile, **credentials):
    driver = webdriver.Firefox()
    driver.get(ADDRESS + htmlfile)
    for key in credentials:
        elem = driver.find_element_by_name(key)
        elem.clear()
        elem.send_keys(credentials[key])
    elem.send_keys(Keys.RETURN)

def go():
    do_login("twofabuster.html", Username="pepe", Password="password")
    do_login("authtoken.html", Password=1234)

go()