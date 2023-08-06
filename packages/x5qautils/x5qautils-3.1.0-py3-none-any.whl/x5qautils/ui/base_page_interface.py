import datetime
import re

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePageInterface:

    def __init__(self, app):
        self.app = app

    #  Поиск элементов ########
    @allure.step('Поиск элемента')
    def find_element(self, *locator):
        return self.app.wd.find_element(*locator)

    @allure.step('Поиск элементов')
    def find_elements(self, *locator) -> list:
        return self.app.wd.find_elements(*locator)

    #  Клик по элементам ########
    @allure.step('Клик по элементу')
    def click(self, locator):
        self.wait_for_click(locator).click()

    @allure.step('Двойной клик по элементу')
    def double_click(self, locator):
        element = self.wait_for_click(locator)
        actions = ActionChains(self.app.wd)
        actions.move_to_element(element)
        actions.double_click(element)
        actions.perform()

    @allure.step('Клик по всем найденным элементам')
    def click_on_all_found_elements(self, *locator):
        elements = self.find_elements(*locator)
        for i in elements:
            self.wait_for_click(locator)
            i.click()

    @allure.step('Клик по координатам')
    def click_with_coord(self, x: int, y: int):
        actions = ActionChains(self.app.wd)
        actions.move_by_offset(x, y).click()

    @allure.step('Клик по элементу правой кнопкой мыши')
    def rbm_click_element(self, locator):
        element = self.find_element(*locator)
        action = ActionChains(self.app.wd)
        action.context_click(element).perform()
        return element

    #  Работа с текстовыми полями ########

    @allure.step('Очистить поле ввода')
    def clear(self, locator):
        element = self.wait_for_click(locator)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)

    @allure.step('Ввод текста в элемент')
    def send_keys(self, locator, text: str):
        self.click(locator)
        self.find_element(*locator).send_keys(text)

    def send_keys_secret(self, locator, text: str):
        """ Метод для скрытия передаваемых параметров в allure-отчете
        """
        with allure.step('Ввод текста в элемент'):
            self.click(locator)
            self.find_element(*locator).send_keys(text)

    @allure.step('Ввод текста/нажатие клавиш n раз')
    def make_n_presses_from_element(self, button, locator, n=1):
        for _ in range(n):
            self.app.wd.find_element(*locator).send_keys(button)

    #  Навигация по страницам ########
    @allure.step('Открытие страницы')
    def open(self, url: str):
        self.app.wd.get(f"{self.app.base_url}{url}")

    @allure.step('Переключение на другую вкладку по номеру вкладки')
    def switch_to_tab(self, tab_num: int):
        new_tab = self.app.wd.window_handles[tab_num]
        self.app.wd.switch_to.window(new_tab)

    #  Работа с системными клавишами ########
    @allure.step('Нажатие системных клавиш')
    def send_system_keys(self, key):
        actions = ActionChains(self.app.wd)
        actions.send_keys(key).perform()

    @allure.step('n нажатий системных клавиш')
    def make_n_presses_system_keys(self, button, n=1):
        for _ in range(n):
            self.send_system_keys(button)

    #  Прокрутка страницы ########
    @allure.step('Скролл к началу страницы')
    def scroll_to_top(self):
        self.app.wd.find_element_by_tag_name('body').send_keys(Keys.HOME)

    @allure.step('Скролл к концу страницы')
    def scroll_to_bottom(self):
        self.app.wd.find_element_by_tag_name('body').send_keys(Keys.END)

    @allure.step('n нажатий клавиш Влево')
    def scroll_to_left_with_keys_n_times(self, n: int, locator):
        self.make_n_presses_from_element(Keys.LEFT, locator, n)

    @allure.step('n нажатий клавиш Вправо')
    def scroll_to_right_with_keys_n_times(self, n: int, locator):
        self.make_n_presses_from_element(Keys.RIGHT, locator, n)

    @allure.step('n нажатий клавиш Вниз')
    def scroll_down_with_keys_n_times(self, n: int, locator):
        self.make_n_presses_from_element(Keys.DOWN, locator, n)

    @allure.step('n нажатий клавиш Вверх')
    def scroll_up_with_keys_n_times(self, n: int, locator):
        self.make_n_presses_from_element(Keys.UP, locator, n)

    @allure.step("Скролл страницы до элемента")
    def scroll_to_element(self, locator):
        element = self.find_element(*locator)
        actions = ActionChains(self.app.wd)
        actions.move_to_element(element).perform()

    #  Работа с drag&drop ########
    @allure.step('Перемещение элемента')
    def move(self, locator_source, locator_target):
        source = self.find_element(*locator_source)
        target = self.find_element(*locator_target)
        ActionChains(self.app.wd).click_and_hold(source).perform()
        ActionChains(self.app.wd).release(target).perform()

    #  Работа с ожидниями ########
    @allure.step('Ожидание отображения элемента')
    def wait(self, locator):
        return WebDriverWait(self, 30).until(ec.visibility_of_element_located(locator),
                                             message=f'Не дождались отображения элемента {locator}')

    def custom_wait(self, locator, sec: int):
        with allure.step(f'Ожидание отображения элемента {sec} секунд'):
            return WebDriverWait(self, sec).until(ec.visibility_of_element_located(locator),
                                                  message=f'Не дождались отображения элемента {locator}')

    @allure.step('Ожидание скрытия элемента')
    def wait_invis(self, locator):
        return WebDriverWait(self, 30).until(ec.invisibility_of_element_located(locator),
                                             message=f'Не дождались исчезновения элемента {locator}')

    def custom_wait_invis(self, locator, sec: int):
        with allure.step(f'Ожидание скрытия элемента {sec} секунд'):
            return WebDriverWait(self, sec).until(ec.invisibility_of_element_located(locator),
                                                  message=f'Не дождались исчезновения элемента {locator}')

    @allure.step('Ожидание кликабельности элемента')
    def wait_for_click(self, locator):
        return WebDriverWait(self, 30).until(ec.element_to_be_clickable(locator),
                                             message=f'Не дождались кликабельности элемента {locator}')

    #  Позиционировние курсора ########
    @allure.step('Наведение курсора на элемент')
    def hover(self, locator):
        hover = ActionChains(self.app.wd).move_to_element(self.wait(locator))
        hover.perform()

    #  Выполнение скриптов ########
    @allure.step('Выполнение скрипта')
    def exec_script(self, script: str):
        self.app.wd.execute_script(script)

    #  Проверка наличия элементов на странице ########
    @allure.step('Проверка отображения элементов на странице')
    def are_exist(self, locator) -> bool:
        return len(self.find_elements(*locator)) > 0

    #  Проверка активности элементов ########
    @allure.step('Проверка активности элемента')
    def is_element_enable(self, locator) -> bool:
        return bool(not self.find_element(*locator).get_attribute('disabled'))

    @allure.step('Проверка, что все элементы активны')
    def are_all_elements_enable(self, locator) -> bool:
        elements = self.find_elements(*locator)
        for element in elements:
            if element.get_attribute('disabled'):
                return False
        else:
            return True

    @allure.step('Проверка, что все элементы неактивны')
    def are_all_elements_disable(self, locator) -> bool:
        elements = self.find_elements(*locator)
        for element in elements:
            if not element.get_attribute('disabled'):
                return False
        else:
            return True

    #  Проверка выставленного положения чекбокса ########
    @allure.step('Проверяем, установлен ли чекбокс')
    def is_checked(self, chkbx) -> bool:
        return self.find_element(*chkbx).is_selected()

    #  Получение текста элемента(ов) ########

    @allure.step('Получение текста элемента')
    def get_text(self, locator) -> str:
        return self.wait(locator).text

    @allure.step('Получение текста элемента без символов %,млн,₽')
    def get_text_prepared(self, locator) -> str:
        return re.sub(r'\s|%|млн|₽', r'', self.wait(locator).text)

    @allure.step('Получение текста из списка элементов')
    def get_text_for_list(self, locator) -> list:
        return [i.text for i in self.find_elements(*locator)]

    @allure.step('Получение текста без пробелов из списка элементов')
    def get_text_for_list_without_spaces(self, locator) -> list:
        return [i.text.replace(' ', '') for i in self.find_elements(*locator)]

    #  Проверка наличия текста ########
    @allure.step('Проверка наличия элемента с текстом')
    def is_element_with_text_exist(self, text) -> bool:
        button = By.XPATH, f"//*[text()='{text}']"
        return self.are_exist(button)

    #  Работа с атрибутами ########
    @allure.step('Получить имя атрибута по имени')
    def get_attribute_value(self, locator, attr_name: str) -> str:
        return self.find_element(*locator).get_attribute(attr_name)

    @allure.step('Проверка, что все элементы имеют атрибут')
    def are_all_elements_has_attr(self, locator, attr) -> bool:
        elements = self.find_elements(*locator)
        return bool(all([element.get_attribute(attr) for element in elements]))

    @allure.step('Проверка, что ни один элемент не имеет атрибута')
    def are_all_elements_has_no_attr(self, locator, attr) -> bool:
        elements = self.find_elements(*locator)
        return bool(not [element.get_attribute(attr) for element in elements])

    #  Работа с css property ########
    @allure.step('Получение значение css property')
    def get_css_property(self, locator, css_property: str) -> str:
        return self.find_element(*locator).get_property(css_property)

    #  Получение совпдений/несовпадений с текстом ########
    @allure.step('Получение списка строк, в которых присутствует заданный текст')
    def get_list_by_value(self, value: str, locator) -> list:
        full_list = self.get_text_for_list(locator)
        return [i for i in full_list if value.lower() in i.lower()]

    @allure.step('Получение списка строк без искомого фрагмента текста')
    def get_list_without_values(self, values: list, locator) -> list:
        list_ = self.get_text_for_list(locator)
        for value in values:
            list_without_value = [i for i in list_ if value.lower() not in i.lower()]
            list_ = list_without_value
        return list_

    #  Работа с алертами ########
    @allure.step('Согласиться с алертом')
    def assert_popup(self):
        self.app.wd.switch_to.alert.accept()

    #  Создание скриншота ########
    @allure.step('Скриншот')
    def screenshot(self):
        url = self.app.wd.current_url
        allure.attach(self.app.wd.get_screenshot_as_png(), name=url + "_" + self.get_current_time(),
                      attachment_type=allure.attachment_type.PNG)

    #  Вспомогательные методы ########
    @allure.step('Получение текущих даты-времени (до минут)')
    def get_current_time(self) -> str:
        return datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

    @allure.step('Перевод строки в число с плав точкой')
    @staticmethod
    def string_to_float(val) -> float:
        return float(re.sub('[^0-9,.]', '', val).replace(',', '.'))

    @allure.step('Округление до целого')
    @staticmethod
    def int_round(num) -> int:
        return int(num + (0.5 if num > 0 else -0.5))

    @allure.step('Замена значений в списке')
    @staticmethod
    def replace_values_in_list(full_list, from_, to_) -> list:
        return [n.replace(from_, to_) for n in full_list]
