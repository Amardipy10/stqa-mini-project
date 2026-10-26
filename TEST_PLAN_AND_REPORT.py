# ═══════════════════════════════════════════════════════════════════
#  STQA MINI PROJECT — TEST PLAN & REPORT
#  TaskFlow: Smart Task Manager Web Application
# ═══════════════════════════════════════════════════════════════════
#
#  Project       : TaskFlow — Smart Task Manager
#  Platform      : Web (HTML5, CSS3, JavaScript)
#  Test Tools    : Selenium WebDriver, Python, pytest, pytest-html
#  Browser       : Google Chrome (Headless)
#  Author        : Amardip
#  Date          : October 2026
#
# ═══════════════════════════════════════════════════════════════════


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. INTRODUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
1.1 PURPOSE
-----------
This document describes the Test Plan for the TaskFlow web application.
It identifies features to be tested, the testing approach, bug taxonomy,
regression test strategy, and exploratory testing observations.

1.2 SCOPE
---------
The application under test (AUT) is a client-side Task Manager built 
with HTML, CSS, and JavaScript. It supports:
  • Task CRUD operations (Create, Read, Update, Delete)
  • Task completion toggling
  • Priority levels (High, Medium, Low)
  • Categories (General, Work, Personal, Study, Health)
  • Due dates with overdue detection
  • Search and filtering
  • Sorting (Date, Priority, Alphabetical, Due Date)
  • Dark/Light theme toggle
  • Persistent localStorage storage
  • Responsive design

1.3 SYSTEM ENVIRONMENT
-----------------------
  • Operating System : macOS / Windows / Linux
  • Browser          : Google Chrome (latest) — headless mode for CI
  • Language         : Python 3.10+
  • Test Framework   : pytest 8.x
  • Automation Tool  : Selenium WebDriver 4.x
  • Report Generator : pytest-html 4.x
  • Driver Manager   : webdriver-manager 4.x
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. FEATURES TO BE TESTED
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
┌─────┬─────────────────────────────┬─────────────────────────────────────────┐
│ ID  │ Feature Module              │ Features                                │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F01 │ Task Creation               │ Add task with title, description,       │
│     │                             │ priority, category, and due date        │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F02 │ Form Validation             │ Empty title, short title, duplicate     │
│     │                             │ detection, max-length enforcement       │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F03 │ Task Completion             │ Toggle complete/incomplete via checkbox │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F04 │ Task Editing                │ Edit title, description, priority,      │
│     │                             │ category, due date via modal dialog     │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F05 │ Task Deletion               │ Delete individual tasks                │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F06 │ Bulk Operations             │ Clear all completed tasks              │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F07 │ Search                      │ Real-time search by title/description  │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F08 │ Filtering                   │ All / Pending / Completed / High       │
│     │                             │ Priority via sidebar navigation        │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F09 │ Sorting                     │ Sort by Date / Priority / A-Z / Due    │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F10 │ Theme Toggle                │ Switch between light and dark mode     │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F11 │ Statistics Dashboard        │ Real-time stats: Total, Active,        │
│     │                             │ Completed, Progress percentage         │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F12 │ Data Persistence            │ Tasks saved to localStorage            │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F13 │ Toast Notifications         │ Feedback on add, delete, toggle, edit  │
├─────┼─────────────────────────────┼─────────────────────────────────────────┤
│ F14 │ Responsive Layout           │ Sidebar collapse, mobile-friendly      │
└─────┴─────────────────────────────┴─────────────────────────────────────────┘
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. BUG TAXONOMY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
3.1 BUG CLASSIFICATION BY TYPE
───────────────────────────────
┌──────────────────────┬──────────────────────────────────────────────┐
│ Bug Type             │ Description & Examples                       │
├──────────────────────┼──────────────────────────────────────────────┤
│ Functional           │ Feature does not work as specified            │
│                      │ e.g., Task not saved, filter not applied      │
├──────────────────────┼──────────────────────────────────────────────┤
│ Validation           │ Input not properly validated                  │
│                      │ e.g., Empty title accepted, XSS possible      │
├──────────────────────┼──────────────────────────────────────────────┤
│ UI / Visual          │ Display issues, misalignment, broken layout   │
│                      │ e.g., Overlapping text, wrong colors           │
├──────────────────────┼──────────────────────────────────────────────┤
│ Usability            │ Poor UX, confusing workflow                   │
│                      │ e.g., No feedback on action, unclear labels    │
├──────────────────────┼──────────────────────────────────────────────┤
│ Performance          │ Slow response, lag, memory leaks              │
│                      │ e.g., Slow render with 100+ tasks             │
├──────────────────────┼──────────────────────────────────────────────┤
│ Data / State         │ Data loss, incorrect persistence              │
│                      │ e.g., Tasks lost on refresh, wrong counts     │
├──────────────────────┼──────────────────────────────────────────────┤
│ Compatibility        │ Browser-specific issues                       │
│                      │ e.g., Broken in Firefox, Safari styling        │
├──────────────────────┼──────────────────────────────────────────────┤
│ Accessibility        │ Not usable with assistive tech                │
│                      │ e.g., Missing ARIA labels, no keyboard nav    │
└──────────────────────┴──────────────────────────────────────────────┘

3.2 BUG SEVERITY LEVELS
────────────────────────
  • Critical  : Application crash, data loss, security vulnerability
  • Major     : Feature not working, blocking user workflow
  • Minor     : Feature works but with cosmetic/UX issues
  • Trivial   : Typo, color mismatch, very minor visual issue

3.3 BUG PRIORITY LEVELS
────────────────────────
  • P1 (Urgent)   : Fix immediately — blocks release
  • P2 (High)     : Fix in current sprint
  • P3 (Medium)   : Fix in next sprint
  • P4 (Low)      : Fix when convenient
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. TEST CASE SUMMARY (50 Test Cases)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
┌────────┬──────────────────────────────────────────┬────────────┬──────────┐
│ TC ID  │ Test Case Description                    │ Module     │ Type     │
├────────┼──────────────────────────────────────────┼────────────┼──────────┤
│ TC-001 │ Add task with valid title                │ Add Task   │ Positive │
│ TC-002 │ Empty title shows error                  │ Validation │ Negative │
│ TC-003 │ Short title (< 3 chars) shows error      │ Validation │ Negative │
│ TC-004 │ Add high-priority task                   │ Add Task   │ Positive │
│ TC-005 │ Add task with category                   │ Add Task   │ Positive │
│ TC-006 │ Add task with due date                   │ Add Task   │ Positive │
│ TC-007 │ Duplicate title rejected                 │ Validation │ Negative │
│ TC-008 │ Form resets after submission             │ Add Task   │ Positive │
│ TC-009 │ Stats update after adding                │ Stats      │ Positive │
│ TC-010 │ Add multiple distinct tasks              │ Add Task   │ Positive │
│ TC-011 │ Reset button clears form                 │ Add Task   │ Positive │
│ TC-012 │ Error clears on new input                │ Validation │ Positive │
│ TC-013 │ Toggle task complete                     │ Toggle     │ Positive │
│ TC-014 │ Toggle task back to incomplete           │ Toggle     │ Positive │
│ TC-015 │ Completed task has strikethrough          │ Toggle     │ Positive │
│ TC-016 │ Delete a task                            │ Delete     │ Positive │
│ TC-017 │ Delete last task shows empty state       │ Delete     │ Positive │
│ TC-018 │ Clear completed tasks                    │ Bulk Ops   │ Positive │
│ TC-019 │ Edit modal opens with data               │ Edit       │ Positive │
│ TC-020 │ Save edited task                         │ Edit       │ Positive │
│ TC-021 │ Edit modal validates empty title         │ Edit       │ Negative │
│ TC-022 │ Close modal via X button                 │ Edit       │ Positive │
│ TC-023 │ Close modal via Cancel                   │ Edit       │ Positive │
│ TC-024 │ Filter pending tasks                     │ Filter     │ Positive │
│ TC-025 │ Filter completed tasks                   │ Filter     │ Positive │
│ TC-026 │ Filter high-priority tasks               │ Filter     │ Positive │
│ TC-027 │ "All Tasks" shows everything             │ Filter     │ Positive │
│ TC-028 │ Page title updates on filter             │ Filter     │ Positive │
│ TC-029 │ Sort by priority                         │ Sort       │ Positive │
│ TC-030 │ Sort alphabetically                      │ Sort       │ Positive │
│ TC-031 │ Active sort button highlighted           │ Sort       │ Positive │
│ TC-032 │ Search by title                          │ Search     │ Positive │
│ TC-033 │ Search with no results                   │ Search     │ Negative │
│ TC-034 │ Search is case-insensitive               │ Search     │ Positive │
│ TC-035 │ Clearing search shows all tasks          │ Search     │ Positive │
│ TC-036 │ Toggle dark mode                         │ Theme      │ Positive │
│ TC-037 │ Toggle back to light mode                │ Theme      │ Positive │
│ TC-038 │ Theme icon changes                       │ Theme      │ Positive │
│ TC-039 │ Page title correct                       │ UI         │ Positive │
│ TC-040 │ Logo displayed                           │ UI         │ Positive │
│ TC-041 │ Stats bar visible                        │ UI         │ Positive │
│ TC-042 │ Empty state shown initially              │ UI         │ Positive │
│ TC-043 │ All navigation items present             │ UI         │ Positive │
│ TC-044 │ Sort buttons present                     │ UI         │ Positive │
│ TC-045 │ Toast on task add                        │ Toast      │ Positive │
│ TC-046 │ Toast on task delete                     │ Toast      │ Positive │
│ TC-047 │ Add → Delete → Re-add same title          │ Regression │ Positive │
│ TC-048 │ Complete → Filter pending                 │ Regression │ Positive │
│ TC-049 │ Search + Filter combination              │ Regression │ Positive │
│ TC-050 │ Stats accuracy after mixed ops           │ Regression │ Positive │
└────────┴──────────────────────────────────────────┴────────────┴──────────┘
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. REGRESSION TEST STRATEGY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
5.1 APPROACH
────────────
Regression tests are automated using Selenium WebDriver with pytest.
They are designed to run after any code change to verify that existing
functionality is not broken.

5.2 REGRESSION SUITE (TC-047 to TC-050)
─────────────────────────────────────────
These test cases specifically target scenarios where bugs were previously
found during exploratory testing:

  • TC-047: Verifies task title can be reused after deletion
           (Previously: deleted task's title was still blocked)

  • TC-048: Verifies completed tasks don't appear in pending filter
           (Previously: filter did not refresh after toggle)

  • TC-049: Verifies search works correctly within active filter
           (Previously: search ignored active filter state)

  • TC-050: Verifies stats remain accurate after mixed operations
           (Previously: stats showed stale counts after delete)

5.3 HOW TO RUN REGRESSION TESTS
─────────────────────────────────
  1. Install dependencies:
     $ pip install -r tests/requirements.txt

  2. Run all tests with HTML report:
     $ pytest

  3. Run only regression tests:
     $ pytest tests/test_ui_theme.py::TestRegression -v

  4. Run specific test file:
     $ pytest tests/test_add_task.py -v

  5. View report:
     Open reports/test_report.html in a browser
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. EXPLORATORY TESTING REPORT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
6.1 EXPLORATORY TEST SESSIONS
───────────────────────────────

SESSION 1: Task Creation & Validation
  Charter   : Explore all ways to add tasks and test boundary conditions
  Duration  : 30 minutes
  Findings  :
    ✅ Valid tasks created successfully with all field combinations
    ✅ Empty title properly rejected
    ✅ Short title (< 3 chars) properly rejected
    ✅ Duplicate detection works for active tasks
    🐛 BUG-001 [Minor]: Whitespace-only title passes validation 
                         → Title " " (spaces) accepted as valid
    🐛 BUG-002 [Trivial]: Max-length counter not shown to user
                           → User doesn't know the 100-char limit

SESSION 2: Task Operations (Toggle, Edit, Delete)
  Charter   : Test all task manipulation operations and edge cases
  Duration  : 30 minutes
  Findings  :
    ✅ Toggle correctly marks tasks complete/incomplete
    ✅ Delete removes task and updates counts
    ✅ Edit modal pre-fills all fields correctly
    ✅ Clear completed works as expected
    🐛 BUG-003 [Minor]: Edit modal doesn't check for duplicate titles
                         → Can rename a task to match an existing one
    🐛 BUG-004 [Trivial]: No confirmation dialog before delete
                           → Accidental deletion is irreversible

SESSION 3: Filtering, Sorting & Search
  Charter   : Explore all filtering, sorting, and search combinations
  Duration  : 25 minutes
  Findings  :
    ✅ All 4 filter categories work correctly
    ✅ Sort by priority places High → Medium → Low
    ✅ Alphabetical sort works correctly
    ✅ Search is case-insensitive and real-time
    🐛 BUG-005 [Minor]: Due date sort doesn't handle tasks without dates well
                         → Tasks without due dates appear at the end (expected?)

SESSION 4: Theme, UI & Accessibility
  Charter   : Test visual consistency, theme toggling, and accessibility
  Duration  : 20 minutes
  Findings  :
    ✅ Dark mode applies correctly to all components
    ✅ Theme persists across page refresh (localStorage)
    ✅ Stats update with smooth number animations
    ✅ Toast notifications appear and auto-dismiss
    🐛 BUG-006 [Minor]: Task action buttons (edit/delete) invisible until 
                         hover — not accessible via keyboard navigation
    🐛 BUG-007 [Trivial]: Emoji-based icons may render differently
                           across operating systems

6.2 BUG SUMMARY TABLE
───────────────────────
┌──────────┬──────────┬──────────┬──────────┬──────────────────────────────┐
│ Bug ID   │ Severity │ Priority │ Type     │ Summary                       │
├──────────┼──────────┼──────────┼──────────┼──────────────────────────────┤
│ BUG-001  │ Minor    │ P3       │ Valid.   │ Whitespace-only title accepted│
│ BUG-002  │ Trivial  │ P4       │ UI       │ No char count indicator       │
│ BUG-003  │ Minor    │ P3       │ Valid.   │ Edit allows duplicate titles  │
│ BUG-004  │ Trivial  │ P4       │ UX       │ No delete confirmation        │
│ BUG-005  │ Minor    │ P3       │ Func.    │ Due date sort edge case       │
│ BUG-006  │ Minor    │ P2       │ A11y     │ Action buttons need keyboard  │
│ BUG-007  │ Trivial  │ P4       │ Compat.  │ Emoji rendering differences   │
└──────────┴──────────┴──────────┴──────────┴──────────────────────────────┘
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. TEST EXECUTION INSTRUCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
STEP 1: Install Python Dependencies
    $ cd "Mini Project STQA"
    $ pip install -r tests/requirements.txt

STEP 2: Run All Tests (generates HTML report)
    $ pytest

STEP 3: Run Tests by Category
    $ pytest tests/test_add_task.py -v          # Task creation tests
    $ pytest tests/test_task_operations.py -v   # CRUD operations
    $ pytest tests/test_filter_sort_search.py -v # Filter/Sort/Search
    $ pytest tests/test_ui_theme.py -v          # UI and regression

STEP 4: Run Only Regression Tests
    $ pytest tests/test_ui_theme.py::TestRegression -v

STEP 5: View HTML Test Report
    Open: reports/test_report.html

STEP 6: Open the Web App
    Open: app/index.html in any browser
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. CONCLUSION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
The TaskFlow web application has been thoroughly tested using a combination
of automated Selenium WebDriver tests and manual exploratory testing.

  • 50 automated test cases cover all major features
  • 4 regression tests target previously identified edge cases
  • 7 bugs identified during exploratory testing (0 critical, 0 major)
  • All core features (CRUD, search, filter, sort) work as expected
  • The application is stable for release with minor fixes recommended

Recommendation: PASS with minor fixes (P3/P4 severity bugs)
"""

if __name__ == "__main__":
    import sys
    print("\n" + "=" * 70)
    print("  STQA MINI PROJECT: TEST PLAN, BUG TAXONOMY & EXPLORATORY REPORT")
    print("=" * 70 + "\n")
    
    # Read and print the file's own content cleanly
    with open(__file__, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Clean docstring markers for clean terminal display
    cleaned = content.replace('"""', '')
    print(cleaned)
    print("\n" + "=" * 70)
    print("  Reports generated at:")
    print("  • Selenium HTML Report : reports/test_report.html")
    print("  • Exploratory Report   : reports/exploratory_test_report.html")
    print("  • Selenium IDE Suite   : tests/taskflow_selenium_ide.side")
    print("=" * 70 + "\n")

