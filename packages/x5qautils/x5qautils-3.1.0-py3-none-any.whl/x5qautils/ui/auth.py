import allure

from .base_page_interface import BasePageInterface


class BaseAuthPage(BasePageInterface):
    locator_login: str = ''
    locator_password: str = ''
    locator_submit: str = ''
    locators_error_message: str = ''

    @allure.step("Ввод логина")
    def enter_login(self, login: str, locator_login):
        self.clear(locator_login)
        self.send_keys(locator_login, login)

    def enter_password(self, password: str, locator_password):
        with allure.step("Ввод пароля"):
            self.clear(locator_password)
            self.send_keys_secret(locator_password, password)

    def login(self, login: str, password: str, locator_login, locator_password, locator_submit):
        with allure.step("Авторизация"):
            self.enter_login(login, locator_login)
            self.enter_password(password, locator_password)
            self.click(locator_submit)

    @allure.step("Проверка сообщения о невалидных авторизационных данных")
    def is_error_message_visible(self, locators_error_message) -> bool:
        return self.are_exist(locators_error_message)
