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

time.sleep(5)
search_button = driver.find_element(By.ID, "search_btn")
search_button.click()

# You may need to wait for JavaScript to load after the click
# Here's how you might do it with WebDriverWait and expected_conditions:

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'r_arrow')))

while (True): 
    try:
        right_arrow = driver.find_element(By.CLASS_NAME, "r_arrow")
        result_containers = driver.find_elements_by_class_name(By.CLASS_NAME, "result_container")
        
        for container in result_containers:
            # Each container has 3 columns
            name_and_two_phone_numbers_col = container.find_element(By.CLASS_NAME, "col1")
            address_col = container.find_element(By.CLASS_NAME, "col2")
            opening_hours_col = container.find_element(By.CLASS_NAME, "col3")

            # Operations for column 1
            # Name and phone numbers are in column 1
            name_span = name_and_two_phone_numbers_col.find_element(By.CLASS_NAME, "name")
            telephone_span = name_and_two_phone_numbers_col.find_element(By.CLASS_NAME, "tel")
            
            # Telephone span contains an anchor tag with the href attribute
            name_anchor_tag = name_span.find_element(By.TAG_NAME, "a")

            # URL for the clinic's page
            clinic_special_listing = name_anchor_tag.get_attribute('href')

            # Clinic name 
            clinic_name = name_anchor_tag.text

            # Phone numbers are in the telephone span - the strip removes the &nbsp; 
            # [Translated as space in python]
            telephone_span_anchor_tag = telephone_span.find_element(By.TAG_NAME, "a")
            telephone_number_string = telephone_span_anchor_tag.text.strip()

            fax_number_string = telephone_span.text.strip()
            '''
            fax_number_string is in the format:
                "T."
                <br>
                "F.67581374"

                to simulate this in python, we can use 
                fax_number_string = "T.\nF.67581374"
                To remove unwanted characters, we can use fax_number_string[5:]
            '''
            fax_number_string = fax_number_string[5:]

            # Operations for column 2
            # Address is in column 2
            address_span = address_col.find_element(By.CLASS_NAME, "add")
            address_text = address_span.text.strip().upper()
            '''
            Address text in the format:
                "1 MARITIME SQUARE"
                <br>
                "HARBOURFRONT CENTRE"
                <br>
                "#02-108 Singapore 099253" => This has been switched to uppercase

                to simulate this in python, we can use
                address_text = "1 MARITIME SQUARE\nHARBOURFRONT CENTRE\n#02-108 Singapore 099253"
                All the "\n" will be replaced with ","
            '''
            address_text = address_text.replace("\n", ",")


        right_arrow.click()
    except:
        break

time.sleep(30)


