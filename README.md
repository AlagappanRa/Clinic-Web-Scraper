# Clinic-Web-Scraper

Welcome to Clinic Web Scraper! This tool is designed to scrape clinic data for various clinics in Singapore, 
previously available on https://www.hcidirectory.gov.sg/hcidirectory/. As of 25/10/2023, the website has migrated 
to a different domain, deprecating this script 😧. 

## Prerequisties
1. Python 3.x installed on your system
2. A web browser (preferably Microsoft Edge, as the driver for Microsft Edge is already available with this repository)

## Setup & Installation
1. Download the Repository
You can clone the repository using the following command:
`git clone https://github.com/AlagappanRa/Clinic-Web-Scraper`

2. Navigate to the Repository on Your Local Machine
Navigate to the directory where you cloned the repository:
`cd path_to_directory/Clinic-Web-Scraper`

3. You need to install Selenium for the web scraping functionality. Run the following command:
`pip install selenium`

4. Install Web Driver
For Selenium to work, you'll also need a WebDriver for your browser:

[ChromeDriver](https://sites.google.com/chromium.org/driver/?pli=1) for Chrome
[GeckoDriver](https://github.com/mozilla/geckodriver/releases) for Firefox

Download the appropriate driver, unzip it, and place it in a known location on your system. 
You might need to provide the path to this driver in the script or add it to your system's PATH.

5. Run the Script
If you are using VSCode:

- Open the repository in VSCode
- Ensure you have the Python extension installed in VSCode
- Open the Python script file
- Click the 'Run Python File in Terminal' option (usually present at the top-right corner of the script editor)
- Alternatively, you can run the script from the terminal:
  `python scraper.py`


## Customization and Notes
- Ensure you are respecting the robots.txt of the website when scraping.
- Web scraping may be subject to legal and ethical considerations. Always ensure you have the right to scrape and use the data you're collecting.
- The structure of websites can change over time. If the script stops working, the website's structure might have changed, and the script might need adjustments.

## Contributing
If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Contributions are welcome!

## License
This project is licensed under the MIT License.

Happy scraping! And always remember to scrape responsibly.
