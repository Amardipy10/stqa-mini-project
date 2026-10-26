"""
═══════════════════════════════════════════════════════════════════════
test_filter_sort_search.py — Test Suite: Filtering, Sorting & Search
═══════════════════════════════════════════════════════════════════════
Covers: sidebar navigation filters, sort buttons, search functionality,
        and combined filter+search operations.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestFiltering:
    """Tests for sidebar navigation filtering."""

    # ─── TC-024: Filter Pending Tasks ───
    def test_filter_pending(self, driver, add_sample_task):
        """Verify that 'Pending' filter shows only incomplete tasks."""
        add_sample_task("Pending task")
        add_sample_task("Completed task")

        # Complete one task
        checkboxes = driver.find_elements(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkboxes[0].click()
        time.sleep(0.3)

        # Click Pending filter
        driver.find_element(By.ID, "nav-pending").click()
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 1
        assert "Pending task" in tasks[0].text

    # ─── TC-025: Filter Completed Tasks ───
    def test_filter_completed(self, driver, add_sample_task):
        """Verify that 'Completed' filter shows only completed tasks."""
        add_sample_task("Active one")
        add_sample_task("Done one")

        # Complete one task
        checkboxes = driver.find_elements(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkboxes[0].click()
        time.sleep(0.3)

        # Click Completed filter
        driver.find_element(By.ID, "nav-completed").click()
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 1

    # ─── TC-026: Filter High Priority ───
    def test_filter_high_priority(self, driver, add_sample_task):
        """Verify that 'High Priority' filter shows only high-priority tasks."""
        add_sample_task("Low task", priority="low")
        add_sample_task("High task", priority="high")

        driver.find_element(By.ID, "nav-high").click()
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 1
        assert "High task" in tasks[0].text

    # ─── TC-027: Filter All Shows Everything ───
    def test_filter_all(self, driver, add_sample_task):
        """Verify that 'All Tasks' filter shows all tasks."""
        add_sample_task("Task A")
        add_sample_task("Task B")

        # Switch to pending then back to all
        driver.find_element(By.ID, "nav-pending").click()
        time.sleep(0.2)
        driver.find_element(By.ID, "nav-all").click()
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 2

    # ─── TC-028: Page Title Updates on Filter Change ───
    def test_page_title_updates(self, driver):
        """Verify that the page title changes when switching filters."""
        driver.find_element(By.ID, "nav-pending").click()
        time.sleep(0.2)

        title = driver.find_element(By.ID, "page-title")
        assert title.text == "Pending Tasks"


class TestSorting:
    """Tests for task sorting controls."""

    # ─── TC-029: Sort by Priority ───
    def test_sort_by_priority(self, driver, add_sample_task):
        """Verify that sorting by priority puts high-priority tasks first."""
        add_sample_task("Low prio", priority="low")
        add_sample_task("High prio", priority="high")
        add_sample_task("Med prio", priority="medium")

        driver.find_element(By.ID, "sort-priority").click()
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert "High prio" in tasks[0].text

    # ─── TC-030: Sort Alphabetically ───
    def test_sort_alphabetical(self, driver, add_sample_task):
        """Verify that alphabetical sorting orders tasks A-Z."""
        add_sample_task("Charlie task")
        add_sample_task("Alpha task")
        add_sample_task("Bravo task")

        driver.find_element(By.ID, "sort-alpha").click()
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert "Alpha task" in tasks[0].text
        assert "Bravo task" in tasks[1].text
        assert "Charlie task" in tasks[2].text

    # ─── TC-031: Active Sort Button Highlighted ───
    def test_active_sort_button(self, driver):
        """Verify that the active sort button gets the 'active' class."""
        sort_btn = driver.find_element(By.ID, "sort-priority")
        sort_btn.click()
        time.sleep(0.2)

        assert "active" in sort_btn.get_attribute("class")


class TestSearch:
    """Tests for the search functionality."""

    # ─── TC-032: Search Filters Tasks by Title ───
    def test_search_by_title(self, driver, add_sample_task):
        """Verify that typing in search filters tasks by title match."""
        add_sample_task("Buy milk")
        add_sample_task("Read book")
        add_sample_task("Buy vegetables")

        driver.find_element(By.ID, "search-input").send_keys("Buy")
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 2

    # ─── TC-033: Search with No Results ───
    def test_search_no_results(self, driver, add_sample_task):
        """Verify that searching for a non-existent term shows empty state."""
        add_sample_task("Existing task")

        driver.find_element(By.ID, "search-input").send_keys("xyz123nonexistent")
        time.sleep(0.3)

        empty = driver.find_element(By.ID, "empty-state")
        assert "visible" in empty.get_attribute("class")

    # ─── TC-034: Search is Case Insensitive ───
    def test_search_case_insensitive(self, driver, add_sample_task):
        """Verify that search works regardless of case."""
        add_sample_task("Important Meeting")

        driver.find_element(By.ID, "search-input").send_keys("important")
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 1

    # ─── TC-035: Clearing Search Shows All Tasks ───
    def test_clear_search(self, driver, add_sample_task):
        """Verify that clearing the search input shows all tasks again."""
        add_sample_task("Task One")
        add_sample_task("Task Two")

        search = driver.find_element(By.ID, "search-input")
        search.send_keys("One")
        time.sleep(0.3)

        # Use JS to clear and fire the input event (Selenium's clear() doesn't trigger it)
        driver.execute_script(
            "arguments[0].value = ''; arguments[0].dispatchEvent(new Event('input'));",
            search
        )
        time.sleep(0.5)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 2

