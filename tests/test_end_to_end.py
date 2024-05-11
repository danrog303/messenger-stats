import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_config import tests_config


@pytest.fixture
def browser():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(1)
    yield driver
    # driver.quit()


def test_file_upload(browser):
    browser.get(tests_config["FRONTEND_SERVICE_URL"])
    file_input = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(tests_config["TEST_FILE_PATH"])

    # Wait for the file to be uploaded
    WebDriverWait(browser, 600).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "MuiLinearProgress-root")))

    # Wait for the file to be unzipped
    WebDriverWait(browser, 600).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Unzipping the file"))
    WebDriverWait(browser, 600).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Unzipping completed."))

    # Wait for stats to be parsed
    WebDriverWait(browser, 600).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Reading statistics..."))
    WebDriverWait(browser, 600).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "All statistics parsed."))

    # Assert graphs has shown up
    assert len(browser.find_elements(By.CSS_SELECTOR, ".graphs-section > div")) > 6
