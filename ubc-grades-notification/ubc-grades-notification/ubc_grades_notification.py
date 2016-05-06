from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from smtplib import SMTP
from time import sleep

email_addr = ""
email_pass = ""

ubc_name = ""
ubc_pass = ""


def send_email(recipient, sender, password, msg, host="smtp.gmail.com"):
    server = SMTP(host, 587)
    server.login(sender, password)
    server.sendmail(sender, recipient, msg)
    server.close()


def get_ssc_grades(ssc_username, ssc_password, browser):
    browser.get("https://ssc.adm.ubc.ca/sscportal/servlets/SRVAcademicRecord?context=html?context=html")

    try: # re-login if SSC has timed out
        browser.find_element_by_id("username").send_keys(ssc_username)
        browser.find_element_by_id("password").send_keys(ssc_password)
        browser.find_element_by_name("submit").click()
    except NoSuchElementException:
        pass

    return browser.find_element_by_id("allSessionsGrades").text


driver = webdriver.Firefox() # or ChromeDriver/PhantomJS
previous_marks = get_ssc_grades(ubc_name, ubc_pass, driver)
while True:
    marks = get_ssc_grades(ubc_name, ubc_pass, driver)
    if marks != previous_marks:
        # smtp.live.com is for outlook, leave blank if using gmail
        send_email(email_addr, email_addr, email_pass, marks, "smtp.live.com") 
        print("Marks uploaded. Email sent.")
    previous_marks = marks
    sleep(60*60)
