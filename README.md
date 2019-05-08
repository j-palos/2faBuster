# 2faBuster

## Build

To setup you environment you must create a python 3 virtual environemnt and
install all dependencies:

    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

You will also need the Gecko driver which is a dependency of selenium and is
the web driver used by selenium to navigate the webpages. The Gecko driver
can be found here:

https://github.com/mozilla/geckodriver/releases

Add the Gecko driver to your PATH and ensure that the python script can see
the Gecko driver on its PATH.

# Usage

To run the program run the twofabusters script:

    $ ./twofabusters

