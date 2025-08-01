import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

import redis
import re
import json

geckodriver_path = "/snap/bin/geckodriver"
service = webdriver.FirefoxService(executable_path=geckodriver_path)
from PIL import Image
import pytesseract

pins_to_check = sys.argv[1].split(',')
dict_of_pins = dict.fromkeys(pins_to_check, 'Invalid')

r = redis.Redis()
driver = webdriver.Firefox(service=service)
driver.get("https://itax.kra.go.ke/KRA-Portal/pinChecker.htm")
for pin in dict_of_pins:
  stripped_pin = pin.strip()
  if r.get(f"KRA_PIN_{pin}"):
    dict_of_pins[pin] = "Valid"
    continue
  if not re.search(r'\A[A-Z]\d{9}[A-Z]\Z',stripped_pin):
    dict_of_pins[pin] = "Invalid Format"
    continue
  input_element = driver.find_element(By.ID, 'vo.pinNo')
  input_element.send_keys(pin)
  captcha_image = driver.find_element(By.ID, 'captcha_img')
  screenshot_file = captcha_image.screenshot('captcha_screenshot.png')
  img = Image.open('captcha_screenshot.png')
  text = pytesseract.image_to_string(img, config='--psm 6')
  arithmetic = text.split('?')[0]
  if '+' in arithmetic:
    result = int(arithmetic.split('+')[0]) + int(arithmetic.split('+')[1])
  elif '-' in arithmetic:
    result = int(arithmetic.split('-')[0]) - int(arithmetic.split('-')[1])
  input_element_2 = driver.find_element(By.ID, 'captcahText')
  input_element_2.send_keys(str(result))
  consult_button = driver.find_element(By.ID, 'consult')
  consult_button.click()
  submit_element = wait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "submit")))
  row_head_elements = driver.find_elements(By.CLASS_NAME, 'tablerowhead')
  for i in row_head_elements:
    if i.text == 'An Error has occurred':
      driver.get("https://itax.kra.go.ke/KRA-Portal/pinChecker.htm")
      break
    if i.text == 'PIN Details':
      dict_of_pins[pin] = "Valid"
      r.set(f"KRA_PIN_{pin}", "Valid")
      break
print(json.dumps(dict_of_pins))
driver.close()
