"""Helper functions for test."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from tests.settings import DriverType

from . import settings

TIMEOUT_BUTTON = 2
TIMEOUT_TEXTFIELD = 2

ID_USERNAME_ELEMENT = "username"
ID_PASSWORD_ELEMENT = "password"


# The name used for the username text field
# The id used for the login button
ID_LOGIN_BUTTON_ELEMENT = "login_button"

# The id used for the logout button in the home page
ID_LOGOUT_ELEMENT = "logout_element"


def is_in_login_screen(driver: DriverType) -> None:
    """Check if the driver is currently at the login screen.

    This functions checks if the driver is in the login screen
    by checking if elements specific exist in the login screen.

    Args:
        driver (webdriver): The webdriver that would be checked.
    """
    msg = "It is not in the login screen"
    assert get_element_by_id(driver, ID_USERNAME_ELEMENT) is not None, msg
    assert get_element_by_id(driver, ID_PASSWORD_ELEMENT) is not None, msg


def is_in_home_page(driver: DriverType) -> None:
    """Check if the driver is currently at the home page.

    This functions checks if the driver is in the home page
    by checking if specific elements exist in the login
    screen.

    Args:
        driver (webdriver): The webdriver that would be checked.
    """
    print(driver.current_url)
    assert driver.current_url == settings.HOME_PAGE_URL
    # assert get_element_by_id(driver, ID_LOGOUT_ELEMENT) is not None


def try_login(driver: DriverType, username: str, password: str) -> None:
    """Try to login to the homepage.

    This functions tries to login to the home page.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        driver (webdriver): The webdriver that would be used.
    """
    # Find the username text field and right the username
    # there and wait.
    username_text_field: WebElement = get_element_by_id(driver, ID_USERNAME_ELEMENT)
    username_text_field.clear()
    username_text_field.send_keys(username)

    # Find the password text field and right the password
    # there and wait.
    password_text_field: WebElement = get_element_by_id(driver, ID_PASSWORD_ELEMENT)
    password_text_field.clear()
    password_text_field.send_keys(password)

    # Find the login button and wait.
    login_button = get_element_by_id(driver, ID_LOGIN_BUTTON_ELEMENT)
    login_button.click()


def get_element_by_id(driver: DriverType, element_id: str) -> WebElement:
    """Get element by their id.

    This function would try to get the element by id. If the
    element does now show up after settings.NORMAL_TIMEOUT
    it will raise an error.

    Args:
        element_id (str): The element id.
        driver (webdriver): The driver that would be used.
    """
    msg_not_found = f"The element with the element id {{{element_id}}} was not found"
    msg_found_multiple = f"There was multiple element with the id {{{element_id}}} found."

    try:
        # Wait until we found a button with the given id
        WebDriverWait(driver, timeout=settings.NORMAL_TIMEOUT).until(
            ec.visibility_of_element_located((By.ID, element_id))
        )
    except TimeoutException as exception:
        raise AssertionError(msg_not_found) from exception

    # Finding the button, check that we only found one and click it!
    elements: list[WebElement] = driver.find_elements(By.ID, element_id)
    assert not len(elements) > 1, msg_found_multiple
    return elements[0]


def get_element_by_css_selector(driver: DriverType, css_selector: str) -> WebElement:
    """Get element using a css selector.

    Args:
        driver (webdriver): The webdriver to use.
        css_selector (str): The css slector to use. This
        can be copied from your browser's web tools when
        inspecting the relevant element.

    Raises:
        AssertionError: If the element could not be located
        within a normal timeout.

    Returns:
        WebElement: The element.
    """
    msg_not_found = f"No elements were found using the css selector {{{css_selector}}}."
    msg_found_multiple = f"Multiple elements were found using the css selector {{{css_selector}}}."

    try:
        # Wait until we found a button with the given id
        WebDriverWait(driver, timeout=settings.NORMAL_TIMEOUT).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
    except TimeoutException as exception:
        raise AssertionError(msg_not_found) from exception

    # Finding the button, check that we only found one and click it!
    elements: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, css_selector)
    assert not len(elements) > 1, msg_found_multiple
    return elements[0]
