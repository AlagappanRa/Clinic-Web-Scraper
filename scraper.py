# @author: Alagappan Ramanthan <github.com/AlagappanRa>
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

# Wait for JavaScript to load after the click
# Used WebDriverWait and expected_conditions:

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

            # @TODO: Phone numbers inconsistent
            # Some F. 0 and some F. 00000000 and some only have F no T
            # Phone numbers are in the telephone span - the strip removes the &nbsp; 
            # [Translated as space in python]
            telephone_span_anchor_tag = telephone_span.find_element(By.TAG_NAME, "a")
            fax_number_string = telephone_span.text.strip()
            '''
            fax_number_string is in the format:
            <If anchor tag exists>
                fax_number_string = " T.  8218092682180926\n F.  0 "
                To remove unwanted characters, we can use fax_number_string[5:]

            <If anchor tag does not exist>
                fax_number_string = " F.  67581374 "
                To remove unwanted characters, we can use fax_number_string[2:]
            '''
            index = fax_number_string.find('F')
            index += 2
            fax_number_string = fax_number_string[index:].strip()
            
            # If there is an anchor tag, extract the telephone number and fax number
            if telephone_span_anchor_tag != None:
                telephone_number_string = telephone_span_anchor_tag.text.strip()

            # Cleaning up the fax number as the fax number could be 0 or 00000000, both will be represented as None
            if (int(fax_number_string) == 0):
                fax_number_string = None

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

            # Operations for column 3
            # Opening hours are in column 3

            '''
            Values in col3 are either: No <strong> tags or <strong> tags
            No <strong> tags => "Please call the clinic for operating hours"
            This will be represented as None, and subseqently when the DictWriter writes to the CSV, it will be an empty cell, or ...,,... in the CSV [where in between the commas is an empty cell]
            '''
            opening_hours_time_span = opening_hours_col.find_element(By.CLASS_NAME, "time")
            opening_hours_strong_tags = opening_hours_time_span.find_elements(By.TAG_NAME, "strong")

            # No strong tags means no opening hours
            if (len(opening_hours_strong_tags) == 0):
                opening_hours = None
            else:
                timings = opening_hours_time_span.text
                '''
                timings is in the format:
                'Public Holiday :  Closed\nMonday to Friday : 08:00 am to 02:00 pm, 05:00 pm to 08:30 pm\nSaturday : 08:00 am to 02:00 pm\nSunday :  Closed'

                to simulate this in python, we can use:
                timings = " : 08:00 am to 01:00 pm, 02:00 pm to 04:30 pm\n : 08:00 am to 12:30 pm\n : Closed "
                '''
                timings = timings.replace("\n", " | ")

                '''
                timings is in the format:
                'Public Holiday :  Closed | Monday to Friday : 08:00 am to 02:00 pm, 05:00 pm to 08:30 pm | Saturday : 08:00 am to 02:00 pm | Sunday : Closed'
                '''

        right_arrow.click()
    except:
        break

time.sleep(30)


