"""Test for navbar functionality."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from tests import helper_test_functions as helper
from tests import settings
from tests.settings import DriverType

NAVBAR_COUNT = 4
NAVBAR_CONTAINER_ID = "main-navbar"
HOME_BUTTON_ID = "home-button-navbar"
DASHBOARD_BUTTON_ID = "dashboards-button-navbar"
SHARED_DASHBOARD_BUTTON_ID = "shared-dashboards-button-navbar"


@pytest.mark.test_navbar_component
class TestNavbarComponent:
    """Class that tests the Navbar component."""

    @pytest.mark.usefixtures("start_server")
    def test_find_navbar(self, browser_driver: DriverType) -> None:
        """Test that a navbar element exists on the page."""
        browser_driver.get(settings.URL)

        WebDriverWait(browser_driver, settings.NORMAL_TIMEOUT).until(
            ec.presence_of_element_located((By.ID, NAVBAR_CONTAINER_ID))
        )

        navbar = browser_driver.find_element(By.ID, NAVBAR_CONTAINER_ID)

        assert navbar, "Navbar could not be found"

    @pytest.mark.usefixtures("start_server")
    def test_find_buttons(self, browser_driver: DriverType) -> None:
        """Test that the navbar items exist on the page."""
        browser_driver.get(settings.URL)
        WebDriverWait(browser_driver, settings.NORMAL_TIMEOUT).until(
            ec.presence_of_element_located((By.ID, NAVBAR_CONTAINER_ID))
        )

        navbar = browser_driver.find_element(By.ID, NAVBAR_CONTAINER_ID)
        navbar_items = navbar.find_elements(By.TAG_NAME, "a")
        navbar_items.extend(navbar.find_elements(By.TAG_NAME, "button"))

        assert len(navbar_items) == NAVBAR_COUNT, "Navbar items do not exist"

    @pytest.mark.usefixtures("start_server")
    def test_redirect(self, browser_driver: DriverType) -> None:
        """Test so Shared Dashboards item redirects to correct page."""
        browser_driver.get(settings.URL)

        # redirect dashboard page
        self.redirect_navbar(
            browser_driver,
            DASHBOARD_BUTTON_ID,
            settings.DASHBOARDS_PAGE_URL,
            "List of dashboard page",
        )

        # redirect shared navbar
        self.redirect_navbar(
            browser_driver,
            SHARED_DASHBOARD_BUTTON_ID,
            settings.SHARED_DASHBOARDS_PAGE_URL,
            "Shared dashboard page",
        )

        # redirect shared navbar
        self.redirect_navbar(
            browser_driver, HOME_BUTTON_ID, settings.HOME_PAGE_URL, "The website home page"
        )

    def redirect_navbar(
        self, browser_driver: DriverType, element_id: str, browser_url: str, page: str
    ):
        """Helper to test_redirect navbar that presses the element."""
        # Press the dashboard button and
        dashboard_button = helper.get_element_by_id(browser_driver, element_id)
        dashboard_button.click()
        assert (
            browser_driver.current_url == browser_url
        ), f"Page did not redirect to the correct {page}"
