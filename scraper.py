# Requirements: pip install selenium
# Download the Edge WebDriver from https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ [And find your correct driver version -> install it in the same folder as this file]
# Microsoft Edge
# Version 114.0.1823.37 (Official build) (64-bit) [my build, if its the same, you can use the local driver]

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge('./edgedriver_win64/msedgedriver.exe') 

# Navigate to the page
driver.get('https://www.hcidirectory.gov.sg')

search_button = driver.find_element(By.ID, "search_btn")
search_button.click()

# You may need to wait for JavaScript to load after the click
# Here's how you might do it with WebDriverWait and expected_conditions:

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'r_arrow')))

while(True): 
    time.sleep(5)


