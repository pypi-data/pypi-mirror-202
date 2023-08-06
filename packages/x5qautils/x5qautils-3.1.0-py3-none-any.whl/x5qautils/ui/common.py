import time

import allure
from selenium.webdriver.common.by import By

from .base_page_interface import BasePageInterface


class BaseCommonHelper(BasePageInterface):
    locator_push_text: str = ''
    locator_checkbox_with_state: str = ''

    #  Работа с текстовыми полями ########

    def fill_text_area(self, input_locator, input_value: str):
        self.send_keys(input_locator, input_value)

    #  Работа с дропдаунами ########

    def fill_select_area(self, select_locator, select_value: str):
        self.hover(select_locator)
        self.click(select_locator)
        val = By.XPATH, f"//div[text()='{select_value}']"
        time.sleep(1)
        self.click(val)

    #  Проверка активности элементов ########

    @allure.step('Проверка активности кнопки с текстом {text}')
    def is_button_enable(self, button_text) -> bool:
        name = By.XPATH, f"//*[text()= '{button_text}']/.."
        return self.is_element_enable(name)

    #  Получение текста элементов ########

    @allure.step('Получение текста из alert-сообщений')
    def get_push_texts(self, locator_push_text) -> list:
        return self.get_text_for_list(locator_push_text)

    #  Работа с таблицами ########

    @allure.step('Получение значений колонки таблицы')
    def get_list_of_values_from_column(self, column_data_qa: str) -> list:
        return self.get_text_for_list(By.XPATH, f"//*[@data-qa-column='{column_data_qa}']")

    @allure.step('Получение списка значений без искомого фрагмента из колонки таблицы')
    def get_list_without_value_from_column(self, values: list, column_name: str) -> list:
        column_ = By.XPATH, f"//*[@data-qa-column='{column_name}']"
        return self.get_list_without_values(values, column_)

    @staticmethod
    @allure.step('Проверка, что все элементы списка {values} равны значению {value}')
    def check_list_equal_to_value(value, values: list) -> bool:
        return bool(all(i == value for i in values))

    @staticmethod
    @allure.step('Проверка поиндексово, что элемент списка 1 больше элемента другого списка 2')
    def comparison_by_index_of_list_values(list_1, list_2) -> bool:
        return all([a > b for a, b in zip(list_1, list_2)])

    @allure.step('Проверка статуса чекбоксов')
    def are_exist_checkboxes_with_state(self, state: str, locator_checkbox_with_state) -> bool:
        return self.are_exist(locator_checkbox_with_state)

    #  Клик по элементам с текстом ########

    @allure.step('Нажатие на элемент с текстом {but_text}')
    def press_element_by_text(self, but_text: str):
        button = By.XPATH, f"//*[text()= '{but_text}']|//*[text()= '{but_text.upper()}']"
        self.click(button)
