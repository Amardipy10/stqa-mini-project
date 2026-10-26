"""
═══════════════════════════════════════════════════════════════════════
test_ui_theme.py — Test Suite: UI Elements, Theme & Accessibility
═══════════════════════════════════════════════════════════════════════
Covers: dark mode toggle, responsive elements, toast notifications,
        keyboard shortcuts, and general UI correctness.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestTheme:
    """Tests for dark/light theme toggle."""

    # ─── TC-036: Toggle Dark Mode ───
    def test_toggle_dark_mode(self, driver):
        """Verify that clicking the theme toggle switches to dark mode."""
        driver.find_element(By.ID, "theme-toggle").click()
        time.sleep(0.3)

        theme = driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme")
        assert theme == "dark"

    # ─── TC-037: Toggle Back to Light Mode ───
    def test_toggle_light_mode(self, driver):
        """Verify that clicking theme toggle twice returns to light mode."""
        toggle = driver.find_element(By.ID, "theme-toggle")
        toggle.click()
        time.sleep(0.2)
        toggle.click()
        time.sleep(0.2)

        theme = driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme")
        assert theme == "light"

    # ─── TC-038: Theme Icon Changes ───
    def test_theme_icon_changes(self, driver):
        """Verify that the theme button icon changes between sun and moon."""
        toggle = driver.find_element(By.ID, "theme-toggle")
        initial_icon = toggle.text

        toggle.click()
        time.sleep(0.2)

        new_icon = toggle.text
        assert initial_icon != new_icon


class TestUIElements:
    """Tests for general UI correctness."""

    # ─── TC-039: Page Title is Correct ───
    def test_page_title(self, driver):
        """Verify the page title is 'TaskFlow — Smart Task Manager'."""
        assert "TaskFlow" in driver.title

    # ─── TC-040: Logo Displayed ───
    def test_logo_displayed(self, driver):
        """Verify that the TaskFlow logo is visible in the sidebar."""
        logo = driver.find_element(By.CSS_SELECTOR, ".logo-text")
        assert logo.is_displayed()
        assert logo.text == "TaskFlow"

    # ─── TC-041: Stats Bar Visible ───
    def test_stats_bar_visible(self, driver):
        """Verify that all 4 stat cards are visible on load."""
        stats = driver.find_elements(By.CSS_SELECTOR, ".stat-card")
        assert len(stats) == 4

    # ─── TC-042: Empty State Shown Initially ───
    def test_empty_state_shown_initially(self, driver):
        """Verify that the empty state message appears when no tasks exist."""
        empty = driver.find_element(By.ID, "empty-state")
        assert "visible" in empty.get_attribute("class")

    # ─── TC-043: All Navigation Items Present ───
    def test_nav_items_present(self, driver):
        """Verify all 4 navigation items are present in the sidebar."""
        nav_items = driver.find_elements(By.CSS_SELECTOR, ".nav-item")
        assert len(nav_items) == 4

    # ─── TC-044: Sort Buttons Present ───
    def test_sort_buttons_present(self, driver):
        """Verify all 4 sort buttons are rendered."""
        sort_btns = driver.find_elements(By.CSS_SELECTOR, ".sort-btn")
        assert len(sort_btns) == 4


class TestToastNotifications:
    """Tests for toast notification behavior."""

    # ─── TC-045: Toast on Task Add ───
    def test_toast_on_add(self, driver, add_sample_task):
        """Verify that a success toast appears after adding a task."""
        add_sample_task("Toast test")
        time.sleep(0.3)

        toasts = driver.find_elements(By.CSS_SELECTOR, ".toast")
        assert len(toasts) >= 1

    # ─── TC-046: Toast on Task Delete ───
    def test_toast_on_delete(self, driver, add_sample_task):
        """Verify that a warning toast appears after deleting a task."""
        add_sample_task("Delete toast")
        time.sleep(0.3)

        delete_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="delete"]')
        driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.5)

        toasts = driver.find_elements(By.CSS_SELECTOR, ".toast")
        assert len(toasts) >= 1


class TestRegression:
    """
    Regression test suite — Ensures previously fixed bugs remain resolved.
    These tests cover edge cases and integration scenarios.
    """

    # ─── TC-047: Add → Delete → Add Same Title ───
    def test_add_delete_readd(self, driver, add_sample_task):
        """Regression: After deleting a task, the same title should be reusable."""
        add_sample_task("Recyclable")
        time.sleep(0.3)

        delete_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="delete"]')
        driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.3)

        # Should be able to re-add
        add_sample_task("Recyclable")
        time.sleep(0.3)

        stat_total = driver.find_element(By.ID, "stat-total")
        assert stat_total.text == "1"

    # ─── TC-048: Complete → Filter Pending → Shows Correct Count ───
    def test_complete_then_filter_pending(self, driver, add_sample_task):
        """Regression: Completing a task and filtering to pending should not show it."""
        add_sample_task("Pending check")
        add_sample_task("Will complete")

        checkboxes = driver.find_elements(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkboxes[0].click()
        time.sleep(0.3)

        driver.find_element(By.ID, "nav-pending").click()
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 1

    # ─── TC-049: Search + Filter Combination ───
    def test_search_with_filter(self, driver, add_sample_task):
        """Regression: Search should work correctly within an active filter."""
        add_sample_task("Work Alpha", priority="high")
        add_sample_task("Work Beta", priority="low")
        add_sample_task("Personal Gamma", priority="high")

        driver.find_element(By.ID, "nav-high").click()
        time.sleep(0.3)
        driver.find_element(By.ID, "search-input").send_keys("Work")
        time.sleep(0.3)

        tasks = driver.find_elements(By.CSS_SELECTOR, ".task-item")
        assert len(tasks) == 1
        assert "Work Alpha" in tasks[0].text

    # ─── TC-050: Stats Accuracy After Mixed Operations ───
    def test_stats_after_mixed_operations(self, driver, add_sample_task):
        """Regression: Stats should remain accurate after add, complete, and delete."""
        add_sample_task("Stat A")
        add_sample_task("Stat B")
        add_sample_task("Stat C")

        # Complete one
        checkboxes = driver.find_elements(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkboxes[0].click()
        time.sleep(0.3)

        # Delete one
        delete_btns = driver.find_elements(By.CSS_SELECTOR, '[data-action="delete"]')
        driver.execute_script("arguments[0].click();", delete_btns[1])
        time.sleep(0.3)

        stat_total = driver.find_element(By.ID, "stat-total")
        stat_active = driver.find_element(By.ID, "stat-active")

        assert stat_total.text == "2"
        assert stat_active.text == "1"
