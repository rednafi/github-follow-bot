import time
from typing import Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from followbot import config


class GHFollow:
    """Bot that follows everyone who follows the target user(s)."""

    def __init__(
        self, yourname: str, yourpass: str, targetname: str, driverpath: str,
    ) -> None:

        # Initializing the headless chrome
        self.yourname = yourname
        self.yourpass = yourpass
        self.targetname = targetname

        # I'm on Linux, so the default chrome driver is for Linux
        self.driver = webdriver.Chrome(driverpath)
        self.driver.get("https://github.com/login")
        self.wait = WebDriverWait(self.driver, 10)

    def _locate_userpass_fields(self) -> Tuple[WebElement, WebElement]:
        """Finds out the username and the password field in the UI."""

        username = self.wait.until(
            EC.presence_of_element_located((By.ID, "login_field"))
        )
        password = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        return username, password

    def _put_username_password(self) -> None:
        """Fills in the username and the password fields with their
        corresponding values."""

        username, password = self._locate_userpass_fields()
        username.send_keys(self.yourname)
        password.send_keys(self.yourpass)

    def _click_signin_button(self) -> None:
        """Locates and clicks the sign in button."""

        login_form = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='Sign in']"))
        )
        login_form.click()

    def _goto_followers_tab(self) -> None:
        """Takes the browser to the followers tab."""

        # Your target user's Github handle goes here
        targetname = self.targetname

        # The function name doesn't reflect it but this also fetches
        # followers' data
        self.driver.get(f"https://github.com/{targetname}?tab=followers")
        time.sleep(2)

    def _find_and_follow(self) -> None:
        # Finds and gathers the followers in a list

        # Get the users elements
        users = self.driver.find_elements_by_xpath("//a[@data-hovercard-type='user']")

        # Getting the links of the followers
        followers = [follower.get_attribute("href") for follower in users]

        # Unique follower links
        followers = list(set(followers))

        # Follow everyone who is following the targetuser
        for user in followers:

            # I know hardcoding the page range is lame but just being
            # lazy for now. Scope for improvement.
            for page in range(1, 5):
                link = f"{user}?page={page}&tab=following"
                self.driver.get(link)

                # Gotta sleep to give it some organic vibe!
                time.sleep(2)

                follow_buttons = self.driver.find_elements_by_xpath(
                    "//input[@aria-label='Follow this person']"
                )

                # I know I'm going to hell for supressing all the errors here.
                # But I've zero ideas what might be the potential exceptions.
                # Care to explore??
                # Will add proper logging here.
                try:
                    for button in follow_buttons:
                        button.submit()
                except Exception:
                    pass

        self.driver.close()

    def assimilate(self) -> None:
        """Assembles and executes all the private methods defined above."""

        self._put_username_password()
        self._click_signin_button()
        self._goto_followers_tab()
        self._find_and_follow()


if __name__ == "__main__":

    # Here goes the list of the Github handles of the users that you want
    # to target
    for targetname in config.TARGET_NAMES_LIST:
        # Instantiate the GHFollow class with your username & password
        # Dont' forget the chrome driver
        bot = GHFollow(
            config.YOUR_NAME, config.YOUR_PASS, targetname, config.CHROME_DRIVER_PATH
        )  # driverpath=default here
        bot.assimilate()
