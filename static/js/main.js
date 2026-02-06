/* Main JavaScript for TodoHub */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

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
});

// Show task details in modal
async function showTaskDetails(taskIdx) {
    try {
        const response = await fetch(`/api/task/${taskIdx}`);
        const data = await response.json();
        
        if (data.success) {
            const modal = new bootstrap.Modal(document.getElementById('taskDetailsModal'));
            
            document.getElementById('taskTitle').textContent = data.task;
            document.getElementById('taskDue').textContent = data.due;
            document.getElementById('taskDescription').textContent = data.description || 'No description';
            document.getElementById('taskStatus').textContent = data.completed ? '✓ Completed' : '◯ Pending';
            
            const priorityBadge = document.getElementById('priorityBadge');
            const colorClass = {
                'OVERDUE': 'bg-danger',
                'HIGH': 'bg-warning',
                'MEDIUM': 'bg-info',
                'LOW': 'bg-success'
            }[data.priority] || 'bg-secondary';
            
            priorityBadge.className = `badge ${colorClass}`;
            priorityBadge.textContent = data.priority;
            
            modal.show();
        }
    } catch (error) {
        console.error('Error fetching task details:', error);
    }
}

// Notification helper
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
    }, 4000);
}

// Export functionality
function exportTasks() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            const dataStr = JSON.stringify(data, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `tasks-${new Date().getTime()}.json`;
            link.click();
        });
}
