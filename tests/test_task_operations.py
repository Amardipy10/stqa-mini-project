"""
═══════════════════════════════════════════════════════════════════════
test_task_operations.py — Test Suite: Task Operations (Toggle, Edit, Delete)
═══════════════════════════════════════════════════════════════════════
Covers: marking complete/incomplete, editing tasks, deleting tasks, 
        clear completed, and related UI updates.
"""

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class TestToggleTask:
    """Tests for marking tasks as complete/incomplete."""

    # ─── TC-013: Mark Task as Completed ───
    def test_toggle_task_complete(self, driver, add_sample_task):
        """Verify that clicking checkbox marks a task as completed."""
        add_sample_task("Test toggle")

        checkbox = driver.find_element(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkbox.click()
        time.sleep(0.3)

        stat_done = driver.find_element(By.ID, "stat-done")
        assert stat_done.text == "1"

    # ─── TC-014: Unmark Completed Task ───
    def test_toggle_task_incomplete(self, driver, add_sample_task):
        """Verify that clicking checkbox again re-opens a completed task."""
        add_sample_task("Toggle back")

        checkbox = driver.find_element(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkbox.click()
        time.sleep(0.3)
        checkbox = driver.find_element(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkbox.click()
        time.sleep(0.3)

        stat_active = driver.find_element(By.ID, "stat-active")
        assert stat_active.text == "1"

    # ─── TC-015: Completed Task Gets Strikethrough ───
    def test_completed_task_has_strikethrough(self, driver, add_sample_task):
        """Verify that completed tasks display with a line-through style."""
        add_sample_task("Check style")

        checkbox = driver.find_element(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkbox.click()
        time.sleep(0.3)

        task_item = driver.find_element(By.CSS_SELECTOR, ".task-item")
        assert "completed" in task_item.get_attribute("class")


class TestDeleteTask:
    """Tests for deleting tasks."""

    # ─── TC-016: Delete a Task ───
    def test_delete_task(self, driver, add_sample_task):
        """Verify that clicking delete removes the task from the list."""
        add_sample_task("Task to delete")

        delete_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="delete"]')
        driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.3)

        stat_total = driver.find_element(By.ID, "stat-total")
        assert stat_total.text == "0"

    # ─── TC-017: Delete Shows Empty State ───
    def test_delete_last_task_shows_empty(self, driver, add_sample_task):
        """Verify that deleting the last task shows the empty state message."""
        add_sample_task("Only task")

        delete_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="delete"]')
        driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.3)

        empty = driver.find_element(By.ID, "empty-state")
        assert "visible" in empty.get_attribute("class")

    # ─── TC-018: Clear Completed Tasks ───
    def test_clear_completed(self, driver, add_sample_task):
        """Verify that 'Clear Completed' removes only completed tasks."""
        add_sample_task("Active task")
        add_sample_task("Done task")

        # Complete the second task
        checkboxes = driver.find_elements(By.CSS_SELECTOR, '[data-action="toggle"]')
        checkboxes[0].click()  # first in list (most recent)
        time.sleep(0.3)

        # Clear completed
        driver.find_element(By.ID, "clear-completed-btn").click()
        time.sleep(0.3)

        stat_total = driver.find_element(By.ID, "stat-total")
        assert stat_total.text == "1"


class TestEditTask:
    """Tests for editing tasks via the modal."""

    # ─── TC-019: Open Edit Modal ───
    def test_edit_modal_opens(self, driver, add_sample_task):
        """Verify that clicking edit opens the modal with pre-filled data."""
        add_sample_task("Editable task", description="Some details")

        edit_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="edit"]')
        driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.3)

        modal = driver.find_element(By.ID, "edit-modal")
        assert "active" in modal.get_attribute("class")

        title_val = driver.find_element(By.ID, "edit-title").get_attribute("value")
        assert title_val == "Editable task"

    # ─── TC-020: Save Edited Task ───
    def test_save_edited_task(self, driver, add_sample_task):
        """Verify that editing and saving updates the task in the list."""
        add_sample_task("Original title")

        edit_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="edit"]')
        driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.3)

        title_field = driver.find_element(By.ID, "edit-title")
        title_field.clear()
        title_field.send_keys("Updated title")

        driver.find_element(By.ID, "save-edit-btn").click()
        time.sleep(0.3)

        task_list = driver.find_element(By.ID, "task-list")
        assert "Updated title" in task_list.text
        assert "Original title" not in task_list.text

    # ─── TC-021: Edit Modal Validates Empty Title ───
    def test_edit_empty_title_error(self, driver, add_sample_task):
        """Verify that saving an edit with empty title shows validation error."""
        add_sample_task("Edit me")

        edit_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="edit"]')
        driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.3)

        title_field = driver.find_element(By.ID, "edit-title")
        title_field.clear()

        driver.find_element(By.ID, "save-edit-btn").click()

        error = driver.find_element(By.ID, "edit-title-error")
        assert error.text != ""

    # ─── TC-022: Close Modal via X Button ───
    def test_close_modal_x_button(self, driver, add_sample_task):
        """Verify that clicking the X button closes the edit modal."""
        add_sample_task("Close test")

        edit_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="edit"]')
        driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.3)

        driver.find_element(By.ID, "modal-close").click()
        time.sleep(0.3)

        modal = driver.find_element(By.ID, "edit-modal")
        assert "active" not in modal.get_attribute("class")

    # ─── TC-023: Close Modal via Cancel Button ───
    def test_close_modal_cancel(self, driver, add_sample_task):
        """Verify that clicking Cancel closes the edit modal."""
        add_sample_task("Cancel test")

        edit_btn = driver.find_element(By.CSS_SELECTOR, '[data-action="edit"]')
        driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.3)

        driver.find_element(By.ID, "cancel-edit-btn").click()
        time.sleep(0.3)

        modal = driver.find_element(By.ID, "edit-modal")
        assert "active" not in modal.get_attribute("class")
