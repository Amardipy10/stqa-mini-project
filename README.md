# 🧪 STQA Mini Project — TaskFlow: Smart Task Manager

## 📋 Project Overview

A web-based **Task Manager** application built to demonstrate Software Testing & Quality Assurance concepts including:

- ✅ Web application development (HTML/CSS/JS)
- ✅ Concise Test Plan with features & bug taxonomy
- ✅ Selenium WebDriver automated test scripts (50 test cases)
- ✅ Regression testing strategy & scripts
- ✅ Exploratory testing with bug reports

---

## 📁 Project Structure

```
Mini Project STQA/
├── app/                                 # Web Application
│   ├── index.html                       # Main HTML
│   ├── styles.css                       # CSS Design System
│   └── app.js                           # Application Logic
├── tests/                               # Selenium Test Scripts
│   ├── conftest.py                      # Shared fixtures (browser setup)
│   ├── requirements.txt                 # Python dependencies
│   ├── test_add_task.py                 # TC-001 to TC-012: Task Creation
│   ├── test_task_operations.py          # TC-013 to TC-023: Toggle/Edit/Delete
│   ├── test_filter_sort_search.py       # TC-024 to TC-035: Filter/Sort/Search
│   ├── test_ui_theme.py                 # TC-036 to TC-050: UI/Theme/Regression
│   └── taskflow_selenium_ide.side       # Selenium IDE Project File
├── reports/                             # Generated Test Reports
│   ├── test_report.html                 # Automated Selenium HTML report
│   └── exploratory_test_report.html     # Exploratory testing & bug taxonomy report
├── pytest.ini                           # Pytest configuration
├── TEST_PLAN_AND_REPORT.py              # Test Plan, Bug Taxonomy & Report Document
└── README.md                            # Project documentation
```

---

## 🚀 How to Run

### 1. Open the Web App
```bash
open app/index.html          # macOS
# or double-click index.html in file explorer
```

### 2. Install Test Dependencies
```bash
pip install -r tests/requirements.txt
```

### 3. Run All Automated Selenium WebDriver Tests
```bash
pytest
```

### 4. Run Specific Test Suite
```bash
pytest tests/test_add_task.py -v           # Task creation
pytest tests/test_task_operations.py -v    # CRUD operations
pytest tests/test_filter_sort_search.py -v # Filters & search
pytest tests/test_ui_theme.py -v           # UI & regression
```

### 5. Run Regression Tests Only
```bash
pytest tests/test_ui_theme.py::TestRegression -v
```

### 6. Run via Selenium IDE
1. Install the **Selenium IDE** Chrome / Firefox extension.
2. Open Selenium IDE and select **Open an existing project**.
3. Choose `tests/taskflow_selenium_ide.side`.
4. Click **Run all tests**.

### 7. View Test Reports
```bash
open reports/test_report.html              # Selenium WebDriver execution report
open reports/exploratory_test_report.html  # Exploratory testing & bug taxonomy report
python3 TEST_PLAN_AND_REPORT.py            # Console output of complete Test Plan
```

---

## 🎯 Features Tested

| Module | Features |
|--------|----------|
| Task Creation | Add with title, description, priority, category, due date |
| Validation | Empty/short title, duplicates, max-length |
| Task Toggle | Mark complete/incomplete with visual feedback |
| Task Edit | Edit all fields via modal dialog |
| Task Delete | Delete individual tasks, clear completed |
| Search | Real-time, case-insensitive search |
| Filter | All / Pending / Completed / High Priority |
| Sort | Date / Priority / A-Z / Due Date |
| Theme | Dark/Light mode with persistence |
| Stats | Live dashboard with total/active/completed/progress |

---

## 🐛 Bugs Found (Exploratory Testing)

| Bug ID | Severity | Description |
|--------|----------|-------------|
| BUG-001 | Minor | Whitespace-only title accepted |
| BUG-002 | Trivial | No character count indicator |
| BUG-003 | Minor | Edit allows duplicate titles |
| BUG-004 | Trivial | No delete confirmation dialog |
| BUG-005 | Minor | Due date sort edge case |
| BUG-006 | Minor | Action buttons need keyboard access |
| BUG-007 | Trivial | Emoji rendering differences across OS |

---

## 🛠 Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Testing**: Python 3.10+, Selenium WebDriver 4.x, pytest 8.x
- **Reports**: pytest-html 4.x
- **Browser**: Google Chrome (headless for CI)
