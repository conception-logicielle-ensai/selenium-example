from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_web_driver():
    driver = webdriver.Firefox()
    return driver


class Authentication:
    def __init__(
        self, cas_username: str, cas_password: str, cas_url: str, moodle_url: str
    ) -> None:
        self.__cas_username = cas_username
        self.__cas_password = cas_password
        self.__cas_url = cas_url
        self.__moodle_url = moodle_url

    def get_auth_url(self) -> str:
        return f"{self.__cas_url}?service={self.__moodle_url}"

    @property
    def cas_username(self):
        return self.__cas_username

    @property
    def cas_password(self):
        return self.__cas_password


def auth(driver, authentication: Authentication) -> None:
    driver.get(authentication.get_auth_url())
    assert "CAS" in driver.title
    elem_username = driver.find_element(By.ID, "username")
    elem_username.send_keys(authentication.cas_username)
    elem_username.send_keys(Keys.RETURN)
    elem_password = driver.find_element(By.ID, "password")
    elem_password.send_keys(authentication.cas_password)
    elem_username.send_keys(Keys.RETURN)
    elem_submit = driver.find_element(By.NAME, "submitBtn")
    elem_submit.send_keys(Keys.ENTER)


def get_moodle_resources(driver) -> str:
    ## TODO aller au bon endroit et itérer / récupérer toute la page?
    return driver.page_source


def load_dotenv_files():
    from dotenv import load_dotenv

    load_dotenv()
    load_dotenv(".env.local", override=True)


if __name__ == "__main__":
    load_dotenv_files()
    import os

    cas_username = os.environ.get("CAS_USERNAME")
    cas_password = os.environ.get("CAS_PASSWORD")
    cas_url = os.environ.get("CAS_URL")
    moodle_url = os.environ.get("MOODLE_URL")
    driver = get_web_driver()
    auth(
        driver=driver,
        authentication=Authentication(
            cas_username=cas_username,
            cas_password=cas_password,
            cas_url=cas_url,
            moodle_url=moodle_url,
        ),
    )
    # Todo : a vous
    resources = get_moodle_resources()
    driver.close()
