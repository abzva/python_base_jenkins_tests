import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pages.elements.calendar_element import CalendarElement


class RegistrationFormPage:

    def __init__(self, driver):
        self.driver = driver
        self.calendar = CalendarElement(driver)

    FIRST_NAME_INPUT = (By.ID, 'firstName')
    LAST_NAME_INPUT = (By.ID, 'lastName')
    EMAIL_INPUT = (By.ID, 'userEmail')
    GENDER = (By.ID, 'genterWrapper')
    MOBILE_INPUT = (By.ID, 'userNumber')
    SUBJECTS_INPUT = (By.ID, 'subjectsInput')
    HOBBIES = (By.ID, 'hobbiesWrapper')
    PICTURE = (By.ID, 'uploadPicture')
    CURRENT_ADDRESS = (By.ID, 'currentAddress')
    STATE = (By.ID, 'state')
    CITY = (By.ID, 'city')
    SUBMIT_BUTTON = (By.ID, 'submit')
    RESULT_FORM = (By.ID, 'resultBody')
    POPUP_CLOSE = (By.CSS_SELECTOR, 'button[aria-label="Close"]')
    STATUS_MESSAGE = (By.ID, 'formError')

    URL = 'https://qa-guru.github.io/one-page-form/automation-practice-form.html'

    def open(self):
        self.driver.get(self.URL)

    def input_first_name(self, first_name):
        input_name = self.driver.find_element(*self.FIRST_NAME_INPUT)
        input_name.send_keys(first_name)

    def input_last_name(self, last_name):
        input_name = self.driver.find_element(*self.LAST_NAME_INPUT)
        input_name.send_keys(last_name)

    def input_email(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def select_gender(self, value):
        if value is None:
            return
        checkbox = self.driver.find_element(By.CSS_SELECTOR, f'input[type="radio"][value="{value}"]')
        checkbox.click()

    def input_mobile_number(self, number):
        input_number = self.driver.find_element(*self.MOBILE_INPUT)
        input_number.send_keys(number)

    def select_subjects(self, *subjects):
        for subject in subjects:
            self.driver.find_element(*self.SUBJECTS_INPUT).send_keys(subject)
            WebDriverWait(self.driver, 5).until(
                ec.visibility_of_element_located((By.CLASS_NAME, 'subjects-auto-complete__option'))
            ).click()

    def select_hobbies(self, *hobbies):
        for hobby in hobbies:
            self.driver.find_element(
                By.CSS_SELECTOR, f'#hobbiesWrapper input[value="{hobby}"]'
            ).click()

    def upload_picture(self, path):
        file_path = os.path.abspath(path)
        self.driver.find_element(*self.PICTURE).send_keys(file_path)

    def input_current_address(self, address):
        self.driver.find_element(*self.CURRENT_ADDRESS).send_keys(address)

    def select_option_by_text(self, trigger_locator, options_class, text):
        element = self.driver.find_element(*trigger_locator)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)
        element.click()
        WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located((By.CLASS_NAME, options_class))
        )
        options = self.driver.find_elements(By.CLASS_NAME, options_class)
        for option in options:
            if option.text == text:
                option.click()
                break

    def select_state(self, state):
        self.select_option_by_text(self.STATE, 'state-city-option', state)

    def select_city(self, city):
        self.select_option_by_text(self.CITY, 'state-city-option', city)

    def clear_first_name(self):
        self.driver.find_element(*self.FIRST_NAME_INPUT).clear()

    def click_button(self):
        element = self.driver.find_element(*self.SUBMIT_BUTTON)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)
        element.click()

    def get_result_text(self):
        return WebDriverWait(self.driver, 5).until(
            ec.visibility_of_element_located(self.RESULT_FORM)
        ).text

    def close_popup(self):
        self.driver.find_element(*self.POPUP_CLOSE).click()

    def wait_for_status_message(self, text):
        return WebDriverWait(
            self.driver,
            timeout=5,
            poll_frequency=0.5
        ).until(
            ec.text_to_be_present_in_element(
                self.STATUS_MESSAGE,
                text
            )
        )
