import random
import pytest
import os
import allure
from datetime import datetime
from pages.registration_form_page import RegistrationFormPage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, '..', 'resources')


@allure.epic("Web Application")
@allure.feature("Registration Form")
class TestRegistrationForm:

    @allure.story("Заполнение только обязательных полей")
    @allure.title("Регистрация с обязательными полями")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_registration_with_required_fields(self, driver):
        page = RegistrationFormPage(driver)
        page.open()

        first_name = 'Gena'
        last_name = 'Litvin'
        gender = 'Female'
        mobile = str(random.randint(7900000000, 7999999999))

        with allure.step("Заполнить обязательные поля"):
            page.close_popup()
            page.input_first_name(first_name)
            page.input_last_name(last_name)
            page.select_gender(gender)
            page.input_mobile_number(mobile)

        with allure.step("Отправить форму"):
            page.click_button()

        with allure.step("Проверить результат"):
            result = page.get_result_text()

        checks = {
            'first_name': first_name in result,
            'last_name': last_name in result,
            'gender': gender in result,
            'mobile': mobile in result,
        }

        failed = [key for key, value in checks.items() if not value]
        assert not failed, f'Не прошли проверки: {failed}'

    @allure.story("Заполнение всех полей формы")
    @allure.title("Регистрация со всеми полями, включая загрузку файла")
    @allure.severity(allure.severity_level.NORMAL)
    def test_registration_form_with_all_fields(self, driver):
        page = RegistrationFormPage(driver)
        page.open()

        first_name = 'Galina'
        last_name = 'Bondar'
        email = 'example@mail.com'
        gender = 'Female'
        mobile = str(random.randint(7900000000, 7999999999))
        day = 3
        month = 'November'
        year = '2000'
        date_of_birth = datetime.strptime(f'{day} {month} {year}', '%d %B %Y').strftime('%d %b %Y')
        subjects = 'Maths', 'English', 'Physics'
        hobbies = 'Sports', 'Reading'
        picture = 'file.pages'
        address = 'г. Санкт-Петербург Невский пр-кт'
        state = 'NCR'
        city = 'Delhi'

        with allure.step("Заполнить все поля формы"):
            page.close_popup()
            page.input_first_name(first_name)
            page.input_last_name(last_name)
            page.input_email(email)
            page.select_gender(gender)
            page.input_mobile_number(mobile)
            page.calendar.select_date_of_birth(day, month, year)
            page.select_subjects(*subjects)
            page.select_hobbies(*hobbies)
            page.upload_picture(os.path.join(RESOURCES_DIR, picture))
            page.input_current_address(address)
            page.select_state(state)
            page.select_city(city)

        with allure.step("Отправить форму"):
            page.click_button()

        with allure.step("Проверить результат"):
            result = page.get_result_text()

        checks = {
            'first_name': first_name in result,
            'last_name': last_name in result,
            'email': email in result,
            'gender': gender in result,
            'mobile': mobile in result,
            'date_of_birth': date_of_birth in result,
            'subjects': all(s in result for s in subjects),
            'picture': picture in result,
            'address': address in result,
            'state': state in result,
            'city': city in result,
        }

        failed = [key for key, value in checks.items() if not value]
        assert not failed, f'Не прошли проверки: {failed}'

    @allure.story("Очистка поля First Name")
    @allure.title("Очистка и повторный ввод имени перед отправкой")
    @allure.severity(allure.severity_level.MINOR)
    def test_clear_first_name_field(self, driver):
        page = RegistrationFormPage(driver)
        page.open()

        first_name = 'Gena'
        new_first_name = 'Mark'
        last_name = 'Litvin'
        gender = 'Female'
        mobile = str(random.randint(7900000000, 7999999999))

        with allure.step("Заполнить форму первоначальным именем"):
            page.close_popup()
            page.input_first_name(first_name)
            page.input_last_name(last_name)
            page.select_gender(gender)
            page.input_mobile_number(mobile)

        with allure.step("Очистить и ввести новое имя"):
            page.clear_first_name()
            page.input_first_name(new_first_name)

        with allure.step("Отправить форму"):
            page.click_button()

        with allure.step("Проверить результат"):
            result = page.get_result_text()

        checks = {
            'first_name': new_first_name in result,
            'last_name': last_name in result,
            'gender': gender in result,
            'mobile': mobile in result,
        }

        failed = [key for key, value in checks.items() if not value]
        assert not failed, f'Не прошли проверки: {failed}'

    @allure.story("Валидация обязательных полей")
    @allure.title("Регистрация без обязательных параметров")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "first_name, last_name, gender, mobile, expected_error",
        [
            pytest.param(
                'Matvei', 'Litvin', 'Female', '',
                'Please fill required fields and enter a valid 10-digit mobile number.',
                id='empty_mobile'
            ),
            pytest.param(
                '', 'Litvin', 'Female', str(random.randint(7900000000, 7999999999)),
                'Please fill required fields and enter a valid First Name.',
                marks=pytest.mark.xfail,
                id='empty_first_name'
            ),
            pytest.param(
                '', 'Litvin', None, str(random.randint(7900000000, 7999999999)),
                'Please fill required fields and enter a valid Gender',
                marks=pytest.mark.xfail,
                id='empty_gender'
            ),
        ]
    )
    def test_registration_without_required_parameters(self, driver, first_name, last_name, gender, mobile,
                                                      expected_error):
        page = RegistrationFormPage(driver)
        page.open()

        with allure.step("Заполнить форму с недостающими обязательными полями"):
            page.close_popup()
            page.input_first_name(first_name)
            page.input_last_name(last_name)
            page.select_gender(gender)
            page.input_mobile_number(mobile)

        with allure.step("Отправить форму"):
            page.click_button()

        with allure.step(f"Проверить сообщение об ошибке: {expected_error}"):
            assert page.wait_for_status_message(expected_error)