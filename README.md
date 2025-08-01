# check_kra_pin_with_selenium
A Python Script that can be used to verify KRA PINs using Selenium as the browser automator

# Requirements
* [Tesseract](https://github.com/tesseract-ocr/tesseract)
* [Pytesseract](https://pypi.org/project/pytesseract/)
* [Selenium](https://www.selenium.dev/documentation/webdriver/)
* [Redis](https://github.com/redis/redis)
* [redis-py](https://github.com/redis/redis-py)

# Usage
Copy the selenium_kra_pin_checker.py file to a location on your path.

Run the script with a single command line argument that accepts the KRA PINS you wish to have verified separated by a comma, eg:
`python3 selenium_kra_pin_checker.py A000000000Z,P000000000Z`

The script will first check if the PIN already exists in the Redis store, check the format of the PIN, and then proceed to verify the PIN at the KRA PIN Checker site. If the PIN is successfully found, it will be added to the Redis store to avoid rechecking valid PINS.






