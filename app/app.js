/* ═══════════════════════════════════════════════════
   TaskFlow — Application Logic
   ═══════════════════════════════════════════════════ */

'use strict';

// ─── State ───
let tasks = [];
let currentFilter = 'all';
let currentSort = 'date';
let editingTaskId = null;

// ─── DOM References ───
const DOM = {
    // Form
    form: document.getElementById('add-task-form'),
    titleInput: document.getElementById('task-title'),
    descInput: document.getElementById('task-description'),
    prioritySelect: document.getElementById('task-priority'),
    categorySelect: document.getElementById('task-category'),
    dueDateInput: document.getElementById('task-due-date'),
    titleError: document.getElementById('title-error'),
    addBtn: document.getElementById('add-task-btn'),
    resetBtn: document.getElementById('reset-form-btn'),

    // Task List
    taskList: document.getElementById('task-list'),
    emptyState: document.getElementById('empty-state'),

    // Navigation
    navItems: document.querySelectorAll('.nav-item'),
    countAll: document.getElementById('count-all'),
    countPending: document.getElementById('count-pending'),
    countCompleted: document.getElementById('count-completed'),
    countHigh: document.getElementById('count-high'),

    // Stats
    statTotal: document.getElementById('stat-total'),
    statActive: document.getElementById('stat-active'),
    statDone: document.getElementById('stat-done'),
    statProgress: document.getElementById('stat-progress'),

    // Header
    pageTitle: document.getElementById('page-title'),
    pageSubtitle: document.getElementById('page-subtitle'),
    searchInput: document.getElementById('search-input'),
    themeToggle: document.getElementById('theme-toggle'),
    menuToggle: document.getElementById('menu-toggle'),
    sidebar: document.getElementById('sidebar'),

    // Sort
    sortBtns: document.querySelectorAll('.sort-btn'),

    // Modal
    editModal: document.getElementById('edit-modal'),
    editForm: document.getElementById('edit-form'),
    editTitle: document.getElementById('edit-title'),
    editDescription: document.getElementById('edit-description'),
    editPriority: document.getElementById('edit-priority'),
    editCategory: document.getElementById('edit-category'),
    editDueDate: document.getElementById('edit-due-date'),
    editTitleError: document.getElementById('edit-title-error'),
    modalClose: document.getElementById('modal-close'),
    cancelEditBtn: document.getElementById('cancel-edit-btn'),

    // Other
    clearCompletedBtn: document.getElementById('clear-completed-btn'),
    toastContainer: document.getElementById('toast-container'),
};

// ═══════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════

function generateId() {
    return 'task_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function formatDate(dateStr) {
    if (!dateStr) return null;
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function isOverdue(dateStr) {
    if (!dateStr) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const due = new Date(dateStr + 'T00:00:00');
    return due < today;
}

function showToast(message, type = 'info') {
    const icons = {
        success: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
        error: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        warning: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        info: '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
    };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span class="toast-icon">${icons[type] || ''}</span><span>${message}</span>`;
    DOM.toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ═══════════════════════════════════════════════════
// LOCAL STORAGE
// ═══════════════════════════════════════════════════

function saveTasks() {
    try {
        localStorage.setItem('taskflow_tasks', JSON.stringify(tasks));
    } catch (e) {
        console.error('Failed to save tasks:', e);
    }
}

function loadTasks() {
    try {
        const stored = localStorage.getItem('taskflow_tasks');
        if (stored) {
            tasks = JSON.parse(stored);
        }
    } catch (e) {
        console.error('Failed to load tasks:', e);
        tasks = [];
    }
}

// ═══════════════════════════════════════════════════
// TASK CRUD OPERATIONS
// ═══════════════════════════════════════════════════

function addTask(title, description, priority, category, dueDate) {
    const task = {
        id: generateId(),
        title: title.trim(),
        description: description.trim(),
        priority,
        category,
        dueDate: dueDate || null,
        completed: false,
        createdAt: new Date().toISOString(),
    };
    tasks.unshift(task);
    saveTasks();
    return task;
}

function deleteTask(id) {
    const idx = tasks.findIndex(t => t.id === id);
    if (idx !== -1) {
        const task = tasks[idx];
        tasks.splice(idx, 1);
        saveTasks();
        return task;
    }
    return null;
}

function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        saveTasks();
        return task;
    }
    return null;
}

function updateTask(id, updates) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        Object.assign(task, updates);
        saveTasks();
        return task;
    }
    return null;
}

function clearCompleted() {
    const count = tasks.filter(t => t.completed).length;
    tasks = tasks.filter(t => !t.completed);
    saveTasks();
    return count;
}

// ═══════════════════════════════════════════════════
// FILTERING & SORTING
// ═══════════════════════════════════════════════════

function getFilteredTasks() {
    let filtered = [...tasks];
    const searchTerm = DOM.searchInput.value.toLowerCase().trim();

    // Apply search filter
    if (searchTerm) {
        filtered = filtered.filter(t =>
            t.title.toLowerCase().includes(searchTerm) ||
            t.description.toLowerCase().includes(searchTerm) ||
            t.category.toLowerCase().includes(searchTerm)
        );
    }

    // Apply category filter
    switch (currentFilter) {
        case 'pending':
            filtered = filtered.filter(t => !t.completed);
            break;
        case 'completed':
            filtered = filtered.filter(t => t.completed);
            break;
        case 'high':
            filtered = filtered.filter(t => t.priority === 'high');
            break;
    }

    // Apply sort
    switch (currentSort) {
        case 'date':
            filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
            break;
        case 'priority': {
            const order = { high: 0, medium: 1, low: 2 };
            filtered.sort((a, b) => order[a.priority] - order[b.priority]);
            break;
        }
        case 'alpha':
            filtered.sort((a, b) => a.title.localeCompare(b.title));
            break;
        case 'due':
            filtered.sort((a, b) => {
                if (!a.dueDate && !b.dueDate) return 0;
                if (!a.dueDate) return 1;
                if (!b.dueDate) return -1;
                return new Date(a.dueDate) - new Date(b.dueDate);
            });
            break;
    }

    return filtered;
}

// ═══════════════════════════════════════════════════
// RENDERING
// ═══════════════════════════════════════════════════

function renderTasks() {
    const filtered = getFilteredTasks();

    if (filtered.length === 0) {
        DOM.taskList.innerHTML = '';
        DOM.emptyState.classList.add('visible');
    } else {
        DOM.emptyState.classList.remove('visible');
        DOM.taskList.innerHTML = filtered.map(task => createTaskHTML(task)).join('');
    }

    updateCounts();
    updateStats();
}

function createTaskHTML(task) {
    const priorityLabels = { high: 'High', medium: 'Medium', low: 'Low' };
    const categoryLabels = {
        general: 'General', work: 'Work',
        personal: 'Personal', study: 'Study', health: 'Health'
    };

    let dueDateTag = '';
    if (task.dueDate) {
        const overdue = isOverdue(task.dueDate) && !task.completed;
        const calSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 4px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`;
        const alertSvg = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -1px; margin-right: 4px;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
        dueDateTag = `<span class="task-tag ${overdue ? 'tag-overdue' : 'tag-due'}">
            ${overdue ? alertSvg + 'Overdue: ' : calSvg}${formatDate(task.dueDate)}
        </span>`;
    }

    return `
        <li class="task-item ${task.completed ? 'completed' : ''}" 
            data-id="${task.id}" 
            data-priority="${task.priority}"
            id="task-${task.id}">
            <label class="task-checkbox">
                <input type="checkbox" ${task.completed ? 'checked' : ''} 
                    data-action="toggle" data-id="${task.id}" 
                    id="checkbox-${task.id}" aria-label="Toggle ${task.title}">
                <span class="checkmark"></span>
            </label>
            <div class="task-content">
                <div class="task-title" id="title-${task.id}">${escapeHTML(task.title)}</div>
                ${task.description ? `<div class="task-description">${escapeHTML(task.description)}</div>` : ''}
                <div class="task-meta">
                    <span class="task-tag tag-priority-${task.priority}">${priorityLabels[task.priority]}</span>
                    <span class="task-tag tag-category">${categoryLabels[task.category]}</span>
                    ${dueDateTag}
                </div>
            </div>
            <div class="task-actions">
                <button class="task-action-btn edit-btn" data-action="edit" data-id="${task.id}" 
                    title="Edit task" id="edit-${task.id}" aria-label="Edit task">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                </button>
                <button class="task-action-btn delete-btn" data-action="delete" data-id="${task.id}" 
                    title="Delete task" id="delete-${task.id}" aria-label="Delete task">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                </button>
            </div>
        </li>
    `;
}

function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function updateCounts() {
    const all = tasks.length;
    const pending = tasks.filter(t => !t.completed).length;
    const completed = tasks.filter(t => t.completed).length;
    const high = tasks.filter(t => t.priority === 'high').length;

    DOM.countAll.textContent = all;
    DOM.countPending.textContent = pending;
    DOM.countCompleted.textContent = completed;
    DOM.countHigh.textContent = high;
}

function updateStats() {
    const total = tasks.length;
    const active = tasks.filter(t => !t.completed).length;
    const done = tasks.filter(t => t.completed).length;
    const progress = total > 0 ? Math.round((done / total) * 100) : 0;

    animateNumber(DOM.statTotal, total);
    animateNumber(DOM.statActive, active);
    animateNumber(DOM.statDone, done);
    DOM.statProgress.textContent = progress + '%';
}

function animateNumber(el, target) {
    const current = parseInt(el.textContent) || 0;
    if (current === target) return;
    el.textContent = target;
    el.style.transform = 'scale(1.2)';
    setTimeout(() => { el.style.transform = 'scale(1)'; el.style.transition = 'transform 0.2s ease'; }, 100);
}

// ═══════════════════════════════════════════════════
// EVENT HANDLERS
// ═══════════════════════════════════════════════════

// ─── Add Task Form ───
DOM.form.addEventListener('submit', (e) => {
    e.preventDefault();

    const title = DOM.titleInput.value.trim();
    const description = DOM.descInput.value.trim();
    const priority = DOM.prioritySelect.value;
    const category = DOM.categorySelect.value;
    const dueDate = DOM.dueDateInput.value;

    // Validation
    if (!title) {
        DOM.titleInput.classList.add('error');
        DOM.titleError.textContent = 'Task title is required';
        DOM.titleInput.focus();
        return;
    }

    if (title.length < 3) {
        DOM.titleInput.classList.add('error');
        DOM.titleError.textContent = 'Title must be at least 3 characters';
        DOM.titleInput.focus();
        return;
    }

    // Check duplicate
    const duplicate = tasks.find(t => t.title.toLowerCase() === title.toLowerCase() && !t.completed);
    if (duplicate) {
        DOM.titleInput.classList.add('error');
        DOM.titleError.textContent = 'An active task with this title already exists';
        DOM.titleInput.focus();
        return;
    }

    addTask(title, description, priority, category, dueDate);
    DOM.form.reset();
    DOM.titleError.textContent = '';
    DOM.titleInput.classList.remove('error');
    renderTasks();
    showToast('Task added successfully!', 'success');
});

// ─── Clear title error on input ───
DOM.titleInput.addEventListener('input', () => {
    DOM.titleInput.classList.remove('error');
    DOM.titleError.textContent = '';
});

// ─── Task List Click Delegation ───
DOM.taskList.addEventListener('click', (e) => {
    const target = e.target.closest('[data-action]');
    if (!target) return;

    const action = target.dataset.action;
    const id = target.dataset.id;

    switch (action) {
        case 'toggle': {
            const task = toggleTask(id);
            if (task) {
                renderTasks();
                showToast(task.completed ? 'Task completed!' : 'Task reopened', task.completed ? 'success' : 'info');
            }
            break;
        }
        case 'edit':
            openEditModal(id);
            break;
        case 'delete': {
            const task = deleteTask(id);
            if (task) {
                renderTasks();
                showToast(`"${task.title}" deleted`, 'warning');
            }
            break;
        }
    }
});

// ─── Navigation ───
DOM.navItems.forEach(item => {
    item.addEventListener('click', () => {
        DOM.navItems.forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        currentFilter = item.dataset.filter;

        const titles = {
            all: 'All Tasks',
            pending: 'Pending Tasks',
            completed: 'Completed Tasks',
            high: 'High Priority'
        };
        const subtitles = {
            all: 'Manage all your tasks in one place',
            pending: 'Tasks that need your attention',
            completed: 'Tasks you\'ve accomplished',
            high: 'Urgent tasks requiring immediate action'
        };

        DOM.pageTitle.textContent = titles[currentFilter];
        DOM.pageSubtitle.textContent = subtitles[currentFilter];
        renderTasks();
    });
});

// ─── Sort ───
DOM.sortBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        DOM.sortBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentSort = btn.dataset.sort;
        renderTasks();
    });
});

// ─── Search ───
DOM.searchInput.addEventListener('input', () => {
    renderTasks();
});

// ─── Theme Toggle ───
function updateThemeToggleUI(isDark) {
    const moonSvg = `<svg class="theme-svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    const sunSvg = `<svg class="theme-svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
    DOM.themeToggle.innerHTML = `${isDark ? sunSvg : moonSvg}<span class="theme-label">${isDark ? 'Light' : 'Dark'}</span>`;
}

DOM.themeToggle.addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const nextTheme = isDark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', nextTheme);
    updateThemeToggleUI(nextTheme === 'dark');
    localStorage.setItem('taskflow_theme', nextTheme);
});

// ─── Mobile Menu Toggle ───
DOM.menuToggle.addEventListener('click', () => {
    DOM.sidebar.classList.toggle('open');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 900 &&
        !DOM.sidebar.contains(e.target) &&
        !DOM.menuToggle.contains(e.target)) {
        DOM.sidebar.classList.remove('open');
    }
});

// ─── Clear Completed ───
DOM.clearCompletedBtn.addEventListener('click', () => {
    const count = clearCompleted();
    if (count > 0) {
        renderTasks();
        showToast(`Cleared ${count} completed task(s)`, 'info');
    } else {
        showToast('No completed tasks to clear', 'warning');
    }
});

// ─── Edit Modal ───
function openEditModal(id) {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    editingTaskId = id;
    DOM.editTitle.value = task.title;
    DOM.editDescription.value = task.description;
    DOM.editPriority.value = task.priority;
    DOM.editCategory.value = task.category;
    DOM.editDueDate.value = task.dueDate || '';
    DOM.editTitleError.textContent = '';
    DOM.editTitle.classList.remove('error');
    DOM.editModal.classList.add('active');
}

function closeEditModal() {
    DOM.editModal.classList.remove('active');
    editingTaskId = null;
}

DOM.editForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const title = DOM.editTitle.value.trim();
    if (!title) {
        DOM.editTitle.classList.add('error');
        DOM.editTitleError.textContent = 'Task title is required';
        return;
    }

    if (title.length < 3) {
        DOM.editTitle.classList.add('error');
        DOM.editTitleError.textContent = 'Title must be at least 3 characters';
        return;
    }

    updateTask(editingTaskId, {
        title,
        description: DOM.editDescription.value.trim(),
        priority: DOM.editPriority.value,
        category: DOM.editCategory.value,
        dueDate: DOM.editDueDate.value || null,
    });

    closeEditModal();
    renderTasks();
    showToast('Task updated successfully!', 'success');
});

DOM.modalClose.addEventListener('click', closeEditModal);
DOM.cancelEditBtn.addEventListener('click', closeEditModal);
DOM.editModal.addEventListener('click', (e) => {
    if (e.target === DOM.editModal) closeEditModal();
});

// ─── Keyboard Shortcuts ───
document.addEventListener('keydown', (e) => {
    // Escape closes modal
    if (e.key === 'Escape') closeEditModal();

    // Ctrl+K focuses search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        DOM.searchInput.focus();
    }
});

// ═══════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════

function init() {
    // Load theme
    const savedTheme = localStorage.getItem('taskflow_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeToggleUI(savedTheme === 'dark');

    // Load tasks
    loadTasks();

    // Set minimum due date to today
    const today = new Date().toISOString().split('T')[0];
    DOM.dueDateInput.setAttribute('min', today);

    // Render
    renderTasks();
}

init();
