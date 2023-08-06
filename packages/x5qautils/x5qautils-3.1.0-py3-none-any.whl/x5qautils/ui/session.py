import allure

from .base_page_interface import BasePageInterface


class BaseSessionHelper(BasePageInterface):
    locator_user_menu_icon: str = ''
    locator_logout_but: str = ''
    locator_login: str = ''

    @allure.step("Логаут")
    def logout(self, locator_user_menu_icon, locator_logout_but):
        self.click(locator_user_menu_icon)
        self.click(locator_logout_but)
        self.wait_invis(locator_user_menu_icon)

    @allure.step("Ожидание успешной авторизации")
    def check_success_login(self, locator_login, locator_user_menu_icon):
        self.wait_invis(locator_login)
        self.wait(locator_user_menu_icon)

    @allure.step("Проверка успешной авторизации")
    def is_user_icon_visible(self, locator_login, locator_user_menu_icon) -> bool:
        self.wait_invis(locator_login)
        return self.are_exist(locator_user_menu_icon)

    @allure.step("Логаут, если авторизован")
    def ensure_logout(self, locator_user_menu_icon, locator_logout_but):
        if self.is_logged_in(locator_user_menu_icon):
            self.logout(locator_user_menu_icon, locator_logout_but)

    def ensure_login(self, user, password, locator_login, locator_user_menu_icon):
        if not self.is_logged_in(locator_user_menu_icon):
            with allure.step("Авторизация, если не авторизован"):
                self.app.auth.login(user, password)
                self.check_success_login(locator_login, locator_user_menu_icon)

    @allure.step("Проверяем, авторизован ли пользователь")
    def is_logged_in(self, locator_user_menu_icon) -> bool:
        self.app.navigation.open_homepage()
        return self.are_exist(locator_user_menu_icon)
