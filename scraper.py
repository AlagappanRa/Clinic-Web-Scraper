# Requirements: pip install selenium
# Download the Edge WebDriver from https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ [And find your correct driver version -> install it in the same folder as this file]
# Microsoft Edge
# Version 114.0.1823.37 (Official build) (64-bit) [my build, if its the same, you can use the local driver]

from selenium import webdriver
import time

driver = webdriver.Edge('./edgedriver_win64/msedgedriver.exe') 

# Navigate to the page
driver.get('https://www.hcidirectory.gov.sg')

# Find the button and click it
search_button = driver.find_element_by_id('search_btn')
search_button.click()

# => move to https://www.hcidirectory.gov.sg/hcidirectory/clinic.do
# Wait for 5 seconds for the JavaScript to load on the site
time.sleep(5)

while True:
    time.sleep(5) 
    #Infinite loop to artificially keep the browser open until a Control C Keyboard Interrupt is sent