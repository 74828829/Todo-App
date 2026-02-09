/* Main JavaScript for TodoHub - Progressive Web App */

let installPromptEvent = null;
let isInstalledApp = false;

document.addEventListener('DOMContentLoaded', async function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Check if app is already installed
    checkIfAppIsInstalled();

    // Make tasks clickable to show details
    document.addEventListener('click', function(e) {
        // Don't trigger modal if clicking on buttons or links
        if (e.target.closest('button') || e.target.closest('a') || e.target.closest('input')) {
            return;
        }
        
        const taskElement = e.target.closest('[data-task-id]');
        if (taskElement) {
            const taskId = taskElement.dataset.taskId;
            showTaskDetails(taskId);
        }
    });

    // Update install button visibility
    setupInstallPrompt();
});

/**
 * Progressive Web App Installation
 */

// Store the beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    installPromptEvent = e;
    showInstallButton();
});

// Listen for app installation success
window.addEventListener('appinstalled', () => {
    console.log('TodoHub app installed successfully');
    hideInstallButton();
    showNotification('TodoHub installed! 🎉 You can now access it from your home screen.', 'success');
});

// Listen for app dismissal
window.addEventListener('beforeinstallprompt', () => {
    const installButton = document.getElementById('installButton');
    if (installButton) {
        installButton.addEventListener('click', async () => {
            if (installPromptEvent) {
                installPromptEvent.prompt();
                const { outcome } = await installPromptEvent.userChoiceProm;
                if (outcome === 'accepted') {
                    console.log('User accepted the install prompt');
                } else {
                    console.log('User dismissed the install prompt');
                }
                installPromptEvent = null;
                hideInstallButton();
            }
        });
    }
});

/**
 * Setup install prompt handlers
 */
function setupInstallPrompt() {
    const installButton = document.getElementById('installButton');
    const installButtonContainer = document.getElementById('installButtonContainer');
    const installPromptConfirm = document.getElementById('installPromptConfirm');

    if (installButton) {
        installButton.addEventListener('click', async () => {
            if (installPromptEvent) {
                // Show the install prompt
                const installModal = new bootstrap.Modal(document.getElementById('installPromptModal'));
                installModal.show();
            }
        });
    }

    if (installPromptConfirm) {
        installPromptConfirm.addEventListener('click', async () => {
            if (installPromptEvent) {
                installPromptEvent.prompt();
                const { outcome } = await installPromptEvent.userChoicePromise;
                if (outcome === 'accepted') {
                    console.log('User accepted the install prompt');
                    const installModal = bootstrap.Modal.getInstance(document.getElementById('installPromptModal'));
                    installModal?.hide();
                    hideInstallButton();
                } else {
                    console.log('User dismissed the install prompt');
                }
                installPromptEvent = null;
            }
        });
    }
}

/**
 * Check if the app is running as an installed PWA
 */
function checkIfAppIsInstalled() {
    const isStandalone = window.navigator.standalone === true ||
                        window.matchMedia('(display-mode: standalone)').matches ||
                        window.matchMedia('(display-mode: fullscreen)').matches;
    
    isInstalledApp = isStandalone;
    console.log('App installed:', isInstalledApp);
    
    if (isInstalledApp) {
        hideInstallButton();
    }
}

/**
 * Show install button in navbar
 */
function showInstallButton() {
    const container = document.getElementById('installButtonContainer');
    if (container) {
        container.classList.remove('d-none');
    }
}

/**
 * Hide install button in navbar
 */
function hideInstallButton() {
    const container = document.getElementById('installButtonContainer');
    if (container) {
        container.classList.add('d-none');
    }
}

/**
 * Priority Calculation Functions
 */

function calculatePriority(dueDateStr) {
    """Calculate priority based on days until due date"""
    try {
        const dueDate = new Date(dueDateStr);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        dueDate.setHours(0, 0, 0, 0);
        
        const daysRemaining = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
        
        if (daysRemaining < 0) {
            return 'OVERDUE';
        } else if (daysRemaining <= 3) {
            return 'HIGH';
        } else if (daysRemaining <= 7) {
            return 'MEDIUM';
        } else {
            return 'LOW';
        }
    } catch (error) {
        return 'N/A';
    }
}

function getPriorityColor(priority) {
    """Return Bootstrap color class for priority"""
    const colors = {
        'OVERDUE': 'danger',
        'HIGH': 'warning',
        'MEDIUM': 'info',
        'LOW': 'success',
        'N/A': 'secondary'
    };
    return colors[priority] || 'secondary';
}

/**
 * Show task details in modal (from IndexedDB)
 */
async function showTaskDetails(taskId) {
    try {
        const task = await todoDb.getTask(taskId);
        
        if (!task) {
            showNotification('Task not found', 'warning');
            return;
        }
        
        const modal = new bootstrap.Modal(document.getElementById('taskDetailsModal'));
        
        document.getElementById('taskTitle').textContent = task.task || 'Untitled';
        document.getElementById('taskDue').textContent = task.due || 'No due date';
        document.getElementById('taskDescription').textContent = task.description || 'No description';
        document.getElementById('taskStatus').textContent = task.completed ? '✓ Completed' : '◯ Pending';
        
        const priorityBadge = document.getElementById('priorityBadge');
        const priority = calculatePriority(task.due);
        const colorClass = getPriorityColor(priority);
        
        priorityBadge.className = `badge bg-${colorClass}`;
        priorityBadge.textContent = priority;
        
        modal.show();
    } catch (error) {
        console.error('Error fetching task details:', error);
        showNotification('Failed to load task details', 'danger');
    }
}

/**
 * Notification helper
 */
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

/**
 * Export tasks from IndexedDB
 */
async function exportTasks() {
    try {
        const exportData = await todoDb.exportTasks();
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `todohub-export-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
        showNotification('Tasks exported successfully', 'success');
    } catch (error) {
        console.error('Export failed:', error);
        showNotification('Failed to export tasks', 'danger');
    }
}

/**
 * Import tasks into IndexedDB
 */
async function importTasks(file) {
    try {
        const text = await file.text();
        const data = JSON.parse(text);
        
        let importedTasks = data.tasks || data;
        if (!Array.isArray(importedTasks)) {
            throw new Error('Invalid import format');
        }

        await todoDb.importTasks(importedTasks);
        showNotification(`Imported ${importedTasks.length} task(s) successfully`, 'success');
        
        // Reload page to show new tasks
        setTimeout(() => location.reload(), 1500);
    } catch (error) {
        console.error('Import failed:', error);
        showNotification('Failed to import tasks: ' + error.message, 'danger');
    }
}

/**
 * Update service worker to latest version
 */
async function updateServiceWorker() {
    if ('serviceWorker' in navigator) {
        try {
            const registration = await navigator.serviceWorker.getRegistrations();
            for (const reg of registration) {
                await reg.update();
            }
            showNotification('TodoHub app updated!', 'info');
        } catch (error) {
            console.error('Service worker update failed:', error);
        }
    }
}

// Check for service worker updates periodically
setInterval(() => {
    updateServiceWorker();
}, 60000); // Check every minute

