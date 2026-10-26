"""
═══════════════════════════════════════════════════════════════════════
test_add_task.py — Test Suite: Task Creation (Add Task Feature)
═══════════════════════════════════════════════════════════════════════
Covers: form validation, successful creation, priority/category, 
        duplicate detection, character limits, and edge cases.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class TestAddTask:
    """Tests for the Add Task functionality."""

    # ─── TC-001: Successful Task Addition ───
    def test_add_task_successfully(self, driver, add_sample_task):
        """Verify that a task can be added with valid title and appears in the list."""
        add_sample_task("Buy groceries", description="Milk, eggs, bread")

        task_list = driver.find_element(By.ID, "task-list")
        assert "Buy groceries" in task_list.text
        assert "Milk, eggs, bread" in task_list.text

    # ─── TC-002: Empty Title Validation ───
    def test_empty_title_shows_error(self, driver):
        """Verify that submitting an empty title shows a validation error."""
        driver.find_element(By.ID, "add-task-btn").click()

        error = driver.find_element(By.ID, "title-error")
        assert error.text == "Task title is required"

    # ─── TC-003: Short Title Validation ───
    def test_short_title_shows_error(self, driver):
        """Verify that a title with fewer than 3 characters shows an error."""
        driver.find_element(By.ID, "task-title").send_keys("ab")
        driver.find_element(By.ID, "add-task-btn").click()

        error = driver.find_element(By.ID, "title-error")
        assert "at least 3 characters" in error.text

    # ─── TC-004: Task with High Priority ───
    def test_add_high_priority_task(self, driver, add_sample_task):
        """Verify that a task can be created with high priority."""
        add_sample_task("Urgent meeting", priority="high")

        task_item = driver.find_element(By.CSS_SELECTOR, '.task-item[data-priority="high"]')
        assert task_item is not None
        assert "Urgent meeting" in task_item.text

    # ─── TC-005: Task with Category ───
    def test_add_task_with_category(self, driver, add_sample_task):
        """Verify that a task shows the correct category tag."""
        add_sample_task("Study for exam", category="study")

        task_list = driver.find_element(By.ID, "task-list")
        assert "Study" in task_list.text

    # ─── TC-006: Task with Due Date ───
    def test_add_task_with_due_date(self, driver, add_sample_task):
        """Verify that a task can be created with a due date."""
        add_sample_task("Submit report", due_date="2027-12-31")

        task_list = driver.find_element(By.ID, "task-list")
        assert "dec 31, 2027" in task_list.text.lower()

    # ─── TC-007: Duplicate Task Detection ───
    def test_duplicate_task_rejected(self, driver, add_sample_task):
        """Verify that adding a duplicate active task shows an error."""
        add_sample_task("Unique task")
        add_sample_task("Unique task")

        error = driver.find_element(By.ID, "title-error")
        assert "already exists" in error.text

    # ─── TC-008: Form Resets After Submission ───
    def test_form_resets_after_submit(self, driver, add_sample_task):
        """Verify that the form clears after a successful task addition."""
        add_sample_task("Test task")

        title_input = driver.find_element(By.ID, "task-title")
        assert title_input.get_attribute("value") == ""

    # ─── TC-009: Stats Update After Adding ───
    def test_stats_update_on_add(self, driver, add_sample_task):
        """Verify that statistics update correctly when a task is added."""
        add_sample_task("First task")

        stat_total = driver.find_element(By.ID, "stat-total")
        assert stat_total.text == "1"

    # ─── TC-010: Multiple Tasks Can Be Added ───
    def test_add_multiple_tasks(self, driver, add_sample_task):
        """Verify that multiple distinct tasks can be added."""
        add_sample_task("Task Alpha")
        add_sample_task("Task Beta")
        add_sample_task("Task Gamma")

        stat_total = driver.find_element(By.ID, "stat-total")
        assert stat_total.text == "3"

    # ─── TC-011: Reset Button Clears Form ───
    def test_reset_button_clears_form(self, driver):
        """Verify that the reset button clears all form fields."""
        driver.find_element(By.ID, "task-title").send_keys("Something")
        driver.find_element(By.ID, "task-description").send_keys("Details")

        driver.find_element(By.ID, "reset-form-btn").click()

        assert driver.find_element(By.ID, "task-title").get_attribute("value") == ""
        assert driver.find_element(By.ID, "task-description").get_attribute("value") == ""

    # ─── TC-012: Error Clears on Input ───
    def test_error_clears_on_new_input(self, driver):
        """Verify that the error message disappears when user starts typing."""
        driver.find_element(By.ID, "add-task-btn").click()
        error = driver.find_element(By.ID, "title-error")
        assert error.text != ""

        driver.find_element(By.ID, "task-title").send_keys("N")
        error = driver.find_element(By.ID, "title-error")
        assert error.text == ""
