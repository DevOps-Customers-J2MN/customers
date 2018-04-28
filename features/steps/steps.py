"""
Customer Steps
Steps file for Customers.feature
"""
from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from app import server

WAIT_SECONDS = 30
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given(u'the following customers')
def step_impl(context):
    """ Delete all Customers and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/customers/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/customers'
    for row in context.table:
        data = {
            "username": row['username'],
            "password": row['password'],
	    "firstname": row["firstname"],
            "lastname": row["lastname"],
            "address": row["address"],
            "phone": row["phone"],
            "email": row["email"]
#            "status": row["status"] in ['1','0'],
#            "promo": row['promo'] in ['1', '0']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)

@when(u'I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    #context.driver.save_screenshot('home_page.png')

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when(u'I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then(u'I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)

@then(u'I should see the message "{message}"')
def step_impl(context, message):
    element = context.driver.find_element_by_id('flash_message')
    expect(element.text).to_contain(message)
    #found = WebDriverWait(context.driver, WAIT_SECONDS).until(
    #    expected_conditions.text_to_be_present_in_element(
    #        (By.ID, 'flash_message'),
    #        message
    #    )
    #)
    #expect(found).to_be(True)

@then(u'I should see "{name}" in the results')
def step_impl(context, name):
#    element = context.driver.find_element_by_id('search_results')
#    expect(element.text).to_contain(name)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)
