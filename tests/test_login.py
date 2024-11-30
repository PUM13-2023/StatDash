"""Test login capabilities of the app."""
import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from tests import helper_test_functions as helper
from tests import settings
from tests.settings import DriverType

# Login credentials for the unvalid test user
WRONG_PASSWORD = "not_valid_user_password"

ID_POP_UP_ELEMENT = "error_input_message"  # The error pop up element id

LOGOUT_BUTTON_ID = "logout-button-navbar"


@pytest.mark.test_login
class TestLogin:
    """A class to group functions to test the login capabilities."""

    @pytest.mark.usefixtures("start_server")
    def test_unsuccessful_login(self, browser_driver: DriverType):
        """Try to login with invalid username and password."""
        browser_driver.get(settings.START_PAGE_URL)

        # Try logging in with wrong password
        helper.try_login(browser_driver, settings.USERS_USERNAME, WRONG_PASSWORD)
        self.check_login_error_pop_up(browser_driver)

    @pytest.mark.usefixtures("start_server")
    def test_successfull_login(self, browser_driver: DriverType):
        """Try to login to the system."""
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(browser_driver, settings.USERS_USERNAME, settings.USERS_PASSWORD)
        # Check that we are still in the homepage after login in
        helper.is_in_home_page(browser_driver)

        # Check that we are still  in the homepage after
        # refreshing in the login page.
        browser_driver.refresh()
        helper.is_in_home_page(browser_driver)

    @pytest.mark.usefixtures("start_server")
    def test_logout(self, browser_driver: DriverType):
        """A test that would try to log out from the system."""
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(browser_driver, settings.USERS_USERNAME, settings.USERS_PASSWORD)

        # Check that we are still in the homepage after logging in
        helper.is_in_home_page(browser_driver)

        # Press the log out button
        logout_button = helper.get_element_by_id(browser_driver, LOGOUT_BUTTON_ID)
        WebDriverWait(browser_driver, timeout=settings.NORMAL_TIMEOUT).until(
            ec.visibility_of(logout_button)
        )

        logout_button.click()

        helper.is_in_login_screen(browser_driver)

    def check_login_error_pop_up(self, driver: DriverType) -> None:
        """Check if the login pop up error is correctly implemented.

        This function test checks if the login pop up error by first
        checking that it exist. After confirming that the error pop
        up exist the function will refresh the browser and after
        that checks that the popup no longer is visible/exist.

        This functions assume that the popup error is
        visible when calling this functions.

        Args:
            driver (DriverType): It is the DriverType in which
            we are going to check if the popup exist.
        """
        # Check if the login error pop up exist and then
        # refresh the site and check that it does not exist.
        pop_up_exist_msg = "There is not any pop error that showed up"
        pop_up_refresh_msg = "There is still a pop up after a refresh"
        assert self.error_pop_up_exist(driver), pop_up_exist_msg
        driver.refresh()
        assert not self.error_pop_up_exist(driver), pop_up_refresh_msg

    def error_pop_up_exist(self, driver: DriverType) -> bool:
        """Check if pop up error exist.

        It will return false if it does not exist and true if the
        popup error exist.

        Args:
            driver (DriverType): It is the DriverType in which
            we are going to

            check if the popup exist.

        Returns:
            bool: True if the popup exist otherwise false.
        """
        # Wait until we found a the element with the pop up id.
        try:
            pop_up = helper.get_element_by_id(driver, ID_POP_UP_ELEMENT)
            return pop_up.is_displayed()
        except Exception:
            return False
