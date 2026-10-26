"""
═══════════════════════════════════════════════════════════
conftest.py — Shared Pytest Fixtures for Selenium Tests
═══════════════════════════════════════════════════════════
Provides browser setup/teardown and common page helpers.
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


# ─── Path to the web application ───
APP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app")
APP_URL = "file://" + os.path.abspath(os.path.join(APP_DIR, "index.html"))


@pytest.fixture(scope="function")
def driver():
    """
    Creates a fresh Chrome WebDriver instance for each test function.
    Opens a VISIBLE browser window so tests can be observed.
    Clears localStorage before each test to ensure a clean state.
    """
    chrome_options = ChromeOptions()
    # NOTE: No --headless flag → browser opens visibly on screen!
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,900")
    chrome_options.add_argument("--disable-gpu")

    service = ChromeService(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(5)

    # Navigate to the app
    browser.get(APP_URL)

    # Clear localStorage for a fresh state
    browser.execute_script("localStorage.clear();")
    browser.refresh()
    browser.get(APP_URL)

    yield browser

    browser.quit()


@pytest.fixture
def add_sample_task(driver):
    """
    Factory fixture that adds a task via the UI and returns a helper function.
    Usage: add_sample_task("My Task", priority="high", category="work")
    """

    def _add_task(title, description="", priority="medium", category="general", due_date=""):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select

        driver.find_element(By.ID, "task-title").clear()
        driver.find_element(By.ID, "task-title").send_keys(title)

        if description:
            driver.find_element(By.ID, "task-description").clear()
            driver.find_element(By.ID, "task-description").send_keys(description)

        Select(driver.find_element(By.ID, "task-priority")).select_by_value(priority)
        Select(driver.find_element(By.ID, "task-category")).select_by_value(category)

        if due_date:
            date_input = driver.find_element(By.ID, "task-due-date")
            date_input.clear()
            driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
                date_input, due_date
            )

        driver.find_element(By.ID, "add-task-btn").click()
        # Wait for the DOM to render the new task
        time.sleep(0.5)

    return _add_task
