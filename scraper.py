# @author: Alagappan Ramanthan <https://github.com/AlagappanRa>
# Requirements: pip install selenium
# Download the Edge WebDriver from https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ [And find your correct driver version -> install it in the same folder as this file]
# Microsoft Edge
# Version 114.0.1823.37 (Official build) (64-bit) [my build, if it's the same, you can use the local driver]

import csv, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge('./edgedriver_win64/msedgedriver.exe') 

# Navigate to the page
driver.get('https://www.hcidirectory.gov.sg')

time.sleep(2)
search_button = driver.find_element(By.ID, "search_btn")
search_button.click()

# Wait for JavaScript to load after the click
# Used WebDriverWait and expected_conditions:

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'r_arrow')))

# Handler function to open the CSV file and return the writer
def get_writer(filename, fieldnames):
    csvfile = open(filename, 'w', newline = '')
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    return csvfile, writer

csvfile, writer = get_writer('clinics.csv', ['ID',
                                             'Clinic Name', 
                                             'Clinic URL', 
                                             'Telephone Number', 
                                             'Fax Number', 
                                             'Address', 
                                             'Opening Hours']
                                             )

def get_clinic_details(global_id):
    # The [1:-1] to ignore the first element and last elements picked up as it shares a similar partial name with "result_container" called "showing results result container"
    result_containers = driver.find_elements(By.CLASS_NAME, "result_container")[1:-1]

    for container in result_containers:
        global_id += 1
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
    
        '''
        @Resolved: Phone numbers inconsistent
        Some F. 0 and some F. 00000000 and some only have F no T
        Cleaning up the fax number as the fax number could be 0 or 00000000, both will be represented as None
        text = "T.  66940100\nF.  65700580"
        OR
        text = "T.  66940100\nF.  0" 
        OR
        text = "F. 0"
        OR
        text = "F. 00000000" 
        '''
        
        text = name_and_two_phone_numbers_col.text.strip()
        telephone_number_string = text[text.find("T.") + 2 : text.find("F.")].strip()
        fax_number_string = text[text.find("F.") + 2 : ].strip()
        if (int(fax_number_string) == 0):
            fax_number_string = ""

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
        address_text = address_text.replace("\n", ", ")
        
        # Operations for column 3
        # Opening hours are in column 3

        '''
        "Please call the clinic for operating hours" will be represented as None, and subseqently when the DictWriter writes to the CSV, it will be an empty cell, or ...,,... in the CSV [where in between the commas is an empty cell]
        '''
        opening_hours_time_span = opening_hours_col.find_element(By.CLASS_NAME, "time")
        opening_span_text = opening_hours_time_span.text.strip()
        if (opening_span_text == "Please call the clinic for operating hours"):
            timings = ""
        else:
            timings = opening_span_text
            timings = timings.replace("\n", " | ")
            '''
            timings is in the format:
            'Public Holiday :  Closed\nMonday to Friday : 08:00 am to 02:00 pm, 05:00 pm to 08:30 pm\nSaturday : 08:00 am to 02:00 pm\nSunday :  Closed'

            to simulate this in python, we can use:
            timings = " : 08:00 am to 01:00 pm, 02:00 pm to 04:30 pm\n : 08:00 am to 12:30 pm\n : Closed "
    
            timings is in the format:
            'Public Holiday :  Closed | Monday to Friday : 08:00 am to 02:00 pm, 05:00 pm to 08:30 pm | Saturday : 08:00 am to 02:00 pm | Sunday : Closed'
            '''

        # Write to CSV
        # Print each attribute to console

        info = {
            'ID': global_id,
            'Clinic Name': clinic_name, 
            'Clinic URL': clinic_special_listing, 
            'Telephone Number': telephone_number_string, 
            'Fax Number': fax_number_string, 
            'Address': address_text, 
            'Opening Hours': timings
            }
        writer.writerow(info)
    return global_id

global_id = 0
while (True): 
    try:
        global_id = get_clinic_details(global_id)
        # Sleep for 1.2 seconds to prevent spamming the server
        time.sleep(1.2) 
        # This should raise an exception at the end as right_arrow element does not exist
        right_arrow = driver.find_element(By.CLASS_NAME, "r_arrow")
        right_arrow.click()

    except Exception as e:
        print(e)
        break

csvfile.close() # this must be executed regardless to prevent memory leak
driver.close() # this must be executed regardless to prevent memory leak