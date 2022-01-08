from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import smtplib
import sys
import time
import os

def cls():
    '''Clears Screen'''
    os.system('cls' if os.name=='nt' else 'clear')

def typer(string,timer=(0.01),remove="no"):
    '''Types out any string passed through (animation)'''
    for c in string:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(timer)
    if remove=="yes":
        cls()

def timedclear(x='',y=1):
    '''Waits for (y) seconds and types out (x) string'''
    time.sleep(y)
    cls()
    typer(x)
    print('')

def getvariables():
    '''Retrieves and stores variables per user needed to check availability of tests'''
    global headless
    global email_address
    global email_password
    global r_email_address
    global driving_license_number
    global application_reference_number
    global test_centre
    
    cls()
    headless=input(f'''\n    - Headless? \n\n    - Type y/n: ''')
    
    timedclear(f'''\n    - Enter credentials for an Email that the program will use to send you notifications regarding test availability!''')
    email_address = str(input(f'''\n    - Email(Sending) \n\n    - Type here: '''))
    email_password = str(input(f'''\n    - Password(Sending) \n\n    - Type here: '''))
    r_email_address = str(input(f'''\n    - Email(Receiving) \n\n    - Type here: '''))
    
    timedclear(f'''\n    - Enter credentials for your DVSA account!''')
    driving_license_number = str(input(f'''\n    - Driving License Number \n\n    - Type here: '''))
    application_reference_number = str(input(f'''\n    - Application Reference Number \n\n    - Type here: '''))
    test_centre = str(input(f'''\n    - Enter the test centre you would like to search within \n\n    - Type here: '''))

def check_availabaility():
    '''Automated DVSA site navigator'''
    if headless=="y":
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    if headless=="n":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #page navigation
    driver.get("https://driverpracticaltest.dvsa.gov.uk/login")
    time.sleep(1)
    search = driver.find_element_by_id("driving-licence-number")
    search.send_keys(driving_license_number)
    time.sleep(1)
    search = driver.find_element_by_id("application-reference-number")
    search.send_keys(application_reference_number)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    search = driver.find_element_by_id("test-centre-change")
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(1)
    search = driver.find_element_by_id("test-centres-input")
    search.clear()
    time.sleep(1)
    search.send_keys(test_centre)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(1)
    search = driver.find_element_by_id("centre-name-131").click()
    #Check whether there are tests available
    try:
        search = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "why-no-slots-help-link"))
        )
    except:
        with smtplib.SMTP ('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_address, email_password)
            subject = 'BOOKING AVAILABLE'
            body = 'GO TO BOOKING'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(email_address, r_email_address, msg)

if __name__ == "__main__":
    cls()
    print('Program is running. . . \n')
    timedclear()
    getvariables()
    check_availabaility()
