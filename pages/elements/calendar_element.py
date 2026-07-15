from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class CalendarElement:

    def __init__(self, driver):
        self.driver = driver

    DATE_OF_BIRTH = (By.ID, 'dateOfBirthInput')
    CALENDAR = (By.ID, 'datepickerDays')
    CALENDAR_MONTH = (By.CSS_SELECTOR, '.react-datepicker__month-select')
    CALENDAR_YEAR = (By.CSS_SELECTOR, '.react-datepicker__year-select')
    CALENDAR_DAY = (By.CSS_SELECTOR, '.react-datepicker__day')

    def select_date_of_birth(self, day, month, year):
        self.driver.find_element(*self.DATE_OF_BIRTH).click()
        Select(self.driver.find_element(*self.CALENDAR_MONTH)).select_by_visible_text(month)
        Select(self.driver.find_element(*self.CALENDAR_YEAR)).select_by_visible_text(str(year))
        self.driver.find_element(By.CSS_SELECTOR, f'[data-day="{day}"]').click()
