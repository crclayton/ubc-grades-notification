from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from smtplib import SMTP
from time import sleep
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("gmail_addr")
parser.add_argument("gmail_pass")
parser.add_argument("ssc_name")
parser.add_argument("ssc_pass")

driver = webdriver.Firefox() # or ChromeDriver/PhantomJS

def send_email(recipient, sender, password, msg, host="smtp.gmail.com"):
    server = SMTP(host, 587)
    server.ehlo()
    server.starttls()
    server.ehlo() 
    server.login(sender, password)
    server.sendmail(sender, recipient, msg)
    server.quit()


def get_ssc_grades(ssc_username, ssc_password, browser):
    browser.get("https://ssc.adm.ubc.ca/sscportal/servlets/SRVAcademicRecord?context=html?context=html")

    try: # re-login if SSC has timed out
        browser.find_element_by_id("username").send_keys(ssc_username)
        browser.find_element_by_id("password").send_keys(ssc_password)
        browser.find_element_by_name("submit").click()
    except NoSuchElementException:
        pass

    return browser.find_element_by_id("allSessionsGrades").text


if __name__ == "__main__":
    args = parser.parse_args()

    ssc_name = args.ssc_name
    ssc_pass = args.ssc_pass
    gmail_addr = args.gmail_addr
    gmail_pass = args.gmail_pass

    # this email is mostly just to check to make sure 
    # the login/email works before relying on the script
    send_email(gmail_addr, gmail_addr, gmail_pass, "UBC Notifications Started") 

    previous_marks = get_ssc_grades(ssc_name, ssc_pass, driver)
    while True:
        marks = get_ssc_grades(ssc_name, ssc_pass, driver)

        if marks != previous_marks:
            send_email(gmail_addr, gmail_addr, gmail_pass, marks) 
            print("Marks uploaded. Email sent.")

        previous_marks = marks
        sleep(60*60)
