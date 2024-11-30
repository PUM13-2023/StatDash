"""Test login capabilities of the app."""

import pytest
from selenium.webdriver.remote.webelement import WebElement
from tests.settings import DriverType

from . import helper_test_functions as helper
from . import settings

# The big create home button
ID_CREATE_DASHBOARD_HOME_BUTTON = "create_dashboard_home"

# On the create dashboard modal.

# The id of the create dashboard modal.
ID_CREATE_DASHBOARD_MODAL = "create_dashboard_modal"
# The cancel button on the modal.
ID_CANCEL_BUTTON_MODAL = "cancel_button_dashboard"
# The create button on the modal.
ID_CREATE_BUTTON_MODAL = "create_button_dashboard"
# The title textfield on the modal.
ID_DASHBOARD_TITLE_FIELD = "dashboard_title_field"
# The desc textfield on the modal.
ID_DESCRIPTION_FIELD = "dashboard_description_field"

# Dashboard page
# the title of the dashboard
ID_DASHBOARD_TITLE = "dashboard_title"

# Dashboards overview page
# The add dashboard button in the dashboard page
ID_ADD_DASHBOARD_BUTTON = "add_dashboard_dashboard_page"


# The name of the dashboard and desc
DASHBOARD_TITLE_1 = "test_dashboard_1"
DASHBOARD_TITLE_2 = "test_dashboard_2"
DASHBOARD_DESC_1 = "testdashboard to test if creating the dashboard works 1"
DASHBOARD_DESC_2 = "testdashboard to test if creating the dashboard works 2"


@pytest.mark.test_create_dashboard
class TestCreateDashboard:
    """A class to group functions to test the dashboard capabilities."""

    @pytest.mark.test_creating_home_page
    @pytest.mark.usefixtures("browser_driver")
    def test_creating_home_page(self, browser_driver: DriverType):
        """Try to create the dashboard from the home screen.

        This function would login the homepage and then press the
        create dashboard button in the home page and then fill
        in the form that popup.

        Args:
            browser_driver(webdriver): The driver that would all test
            would be happening on.
        """
        # Log in to the homepage
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(browser_driver, settings.USERS_USERNAME, settings.USERS_PASSWORD)
        helper.is_in_home_page(browser_driver)

        # Press the create dashboard button and check if the modal is
        # displayed to the user.
        create_dashboard_button: WebElement = helper.get_element_by_id(
            browser_driver, ID_CREATE_DASHBOARD_MODAL
        )
        create_dashboard_button.click()

        dashboard_modal: WebElement = helper.get_element_by_id(
            browser_driver, ID_CREATE_DASHBOARD_MODAL
        )
        assert (
            dashboard_modal.is_displayed()
        ), "The modal was not displayed after pressing the create dashboard button"

        # Press the cancel button and check so the modal is no longer
        # displayed to the user.
        cancel_button = helper.get_element_by_id(browser_driver, ID_CANCEL_BUTTON_MODAL)
        cancel_button.click()
        assert (
            not dashboard_modal.is_displayed()
        ), "The modal was not displayed after pressing the create dashboard button"

        # Test creating the dashboard
        create_dashboard_button.click()
        cancel_button = helper.get_element_by_id(browser_driver, ID_CANCEL_BUTTON_MODAL)
        create_button = helper.get_element_by_id(browser_driver, ID_CREATE_BUTTON_MODAL)
        dashboard_title_field = helper.get_element_by_id(browser_driver, ID_DASHBOARD_TITLE_FIELD)
        dashboard_desc_field = helper.get_element_by_id(browser_driver, ID_DESCRIPTION_FIELD)
        dashboard_title_field.send_keys(DASHBOARD_TITLE_1)
        dashboard_desc_field.send_keys(DASHBOARD_DESC_1)
        create_button.click()

        # Test if the dashboard was created
        self.check_dashboard_created(browser_driver, DASHBOARD_TITLE_1)

    @pytest.mark.test_creating_dashboard_page
    def test_creating_dashboard_page(self, browser_driver: DriverType):
        """Try to create a dashboard from the dashboard page.

        This function would login the homepage and then press the
        create dashboard button in the dashboard page
        and then fill in the form that popup.

        Args:
            browser_driver(webdriver): The driver that would all test
            would be happening on.
        """
        # Log in to the homepage
        browser_driver.get(settings.START_PAGE_URL)
        helper.try_login(browser_driver, settings.USERS_USERNAME, settings.USERS_PASSWORD)
        helper.is_in_home_page(browser_driver)

        # Go to the dashboard screen
        dashboard_button: WebElement = helper.get_element_by_id(
            browser_driver, settings.DASHBOARD_BUTTON_NAV
        )

        dashboard_button.click()

        # Press the create dashboard button and check if the modal is
        # displayed to the user.
        create_dashboard_button: WebElement = helper.get_element_by_id(
            browser_driver, ID_ADD_DASHBOARD_BUTTON
        )

        create_dashboard_button.click()

        dashboard_modal: WebElement = helper.get_element_by_id(
            browser_driver, ID_CREATE_DASHBOARD_MODAL
        )
        assert (
            dashboard_modal.is_displayed()
        ), "The modal was not displayed after pressing the create dashboard button"

        # Test creating the dashboard
        create_dashboard_button.click()
        create_button = helper.get_element_by_id(browser_driver, ID_CREATE_BUTTON_MODAL)
        dashboard_title_field = helper.get_element_by_id(browser_driver, ID_DASHBOARD_TITLE_FIELD)
        dashboard_desc_field = helper.get_element_by_id(browser_driver, ID_DESCRIPTION_FIELD)
        dashboard_title_field.send_keys(DASHBOARD_TITLE_2)
        dashboard_desc_field.send_keys(DASHBOARD_DESC_2)
        create_button.click()

        # Test if the dashboard was created
        self.check_dashboard_created(browser_driver, DASHBOARD_TITLE_2)

    def check_dashboard_created(self, browser_driver: DriverType, dashboard_title: str) -> None:
        """Check if the dashboard was created with the given title.

        This function checks if the created dashboard has the right
        given name. This function assumes that the browser is currently
        inside the dashboard that has been created.

        Args:
            browser_driver (webdriver): It is the webdriver in which
            we are going to check if the popup exist.

            dashboard_title (str): The title of the dashboard that
            was created.

        """
        # Check if the dashboard is created.
        # TODO: can make the check more intensive such as
        # that the newly created dashboard show show up in
        # the home screen.
        dashboard_title_element = helper.get_element_by_id(browser_driver, ID_DASHBOARD_TITLE)
        msg_wrong_title = "The title that was given does not match the title of the dashboard"
        assert dashboard_title_element.text() == dashboard_title, msg_wrong_title
