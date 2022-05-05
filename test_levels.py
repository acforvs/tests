import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import url_matches, url_contains


@pytest.fixture
def driver():
    options = Options()
    options.page_load_strategy = 'normal'
    driver = webdriver.Safari(options=options)
    driver.maximize_window()
    return driver


@pytest.mark.usefixtures('driver')
class TestMainPage:
    def test_is_signin_present(self, driver):
        driver.get('https://www.levels.fyi/')
        signin_button = driver.find_elements(value="//*[@class='action-button login']", by=By.XPATH)
        assert signin_button

    def test_is_signup_present(self, driver):
        driver.get('https://www.levels.fyi/')
        signup_button = driver.find_elements(value="//*[@class='action-button signup']", by=By.XPATH)
        assert signup_button

    def test_is_search_present(self, driver):
        driver.get('https://www.levels.fyi/')
        search_line = driver.find_elements(value="//*[@class='omnisearch-input']", by=By.XPATH)
        assert search_line

    def test_are_companies_present(self, driver):
        driver.get('https://www.levels.fyi/')
        companies = driver.find_elements(value="//*[@class='company-titulo']", by=By.XPATH)
        assert companies

    def test_are_companies_clickable(self, driver):
        driver.get('https://www.levels.fyi/')
        companies = driver.find_elements(value="//*[@class='company-titulo']", by=By.XPATH)

        company_name = companies[0].text
        classname = 'btn-group-vertical btn-group-xs company-name-div'
        companies[0].click()

        WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_elements(value=f"//*[@class='{classname}'][@aria-label='{company_name}']", by=By.XPATH)
        )

    def test_table_is_clickable(self, driver):
        driver.get('https://www.levels.fyi/')
        rows = driver.find_elements(value="//*[@class='levelTable']/tr[1]/td[1]", by=By.XPATH)
        rows[0].click()
        WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(
                value="//*[@class='remodal remodal-is-initialized remodal-is-opened']",
                by=By.XPATH
            )
        )
        assert driver.find_element(value="//*[@class='donut-segment base-donut-segment']", by=By.XPATH)
        table_classname = 'table table-striped table-bordered table-hover breakdown salary-breakdown-table'
        assert driver.find_element(value=f"//*[@class='{table_classname}']/tbody/tr[1]/td[1]", by=By.XPATH).text


@pytest.mark.usefixtures('driver')
class TestSearch:
    company = 'Yandex'

    @staticmethod
    def yandex_present(driver):
        search_results = driver.find_elements(value="//*[@class='omnisearch-results']", by=By.XPATH)
        if not search_results:
            return False
        lis = search_results[0].find_elements(value='li', by=By.TAG_NAME)
        return any('Yandex' in li.text for li in lis)

    @staticmethod
    def yandex_page_opened(driver):
        classname = 'levels-header-grey font-weight-semi-bold mb-1 company-tab-header'
        elements = driver.find_elements(value=f"//*[@class='{classname}']", by=By.XPATH)
        if not elements:
            return False
        return 'Yandex' in elements[0].text

    def test_search(self, driver):
        driver.get('https://www.levels.fyi/')
        search_line = driver.find_element(value="//*[@class='omnisearch-input']", by=By.XPATH)
        search_line.send_keys(self.company)

        WebDriverWait(driver, timeout=5).until(self.yandex_present)

        yandex_result = driver.find_elements(value="//*[@class='omnisearch-results']", by=By.XPATH)[0]
        lis = yandex_result.find_elements(value='li', by=By.TAG_NAME)
        lis[1].click()

        WebDriverWait(driver, timeout=5).until(self.yandex_page_opened)


def test_salary_submission_window(driver):
    driver.get('https://www.levels.fyi/company/Yandex/salaries/Software-Engineer/')
    button = driver.find_element(value="//*[@class='btn btn-sm btn-primary add-comp-btn']", by=By.XPATH)
    button.click()

    classname = 'MuiTypography-root MuiTypography-h4 css-1obfatg'
    WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(value=f"//*[@class='{classname}']", by=By.XPATH)
    )

    assert 'Add Your Salary' == driver.find_element(value=f"//*[@class='{classname}']", by=By.XPATH).text

    button_classname = 'MuiButton-root MuiButton-contained ' \
                       'MuiButton-containedPrimary MuiButton-sizeLarge ' \
                       'MuiButton-containedSizeLarge MuiButton-fullWidth ' \
                       'MuiButtonBase-root css-1tcxuxr'

    button = driver.find_element(value=f"//*[@class='{button_classname}']", by=By.XPATH)
    button.click()
    WebDriverWait(driver, timeout=5).until(
        url_matches('https://www.levels.fyi/salaries/add')
    )
