from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import json
import os
from datetime import datetime, timedelta
import re

app = Flask(__name__)

TODO_FILE = 'todos.json'

# ============================================================================
# UTILITY FUNCTIONS (from main.py)
# ============================================================================

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos):
    try:
        with open(TODO_FILE, 'w') as f:
            json.dump(todos, f, indent=2)
    except IOError:
        return False
    return True

def cleanup_completed(todos):
    """Remove todos that were completed more than 2 days ago."""
    changed = False
    now = datetime.now()
    cutoff = now - timedelta(days=2)
    remaining = []
    for t in todos:
        if t.get('completed') and t.get('completed_at'):
            try:
                completed_at = datetime.fromisoformat(t.get('completed_at'))
                if completed_at < cutoff:
                    changed = True
                    continue
            except Exception:
                pass
        remaining.append(t)
    if changed:
        save_todos(remaining)
    return remaining

def cleanup_deleted(todos):
    """Permanently remove todos that were deleted more than 3 days ago."""
    changed = False
    now = datetime.now()
    cutoff = now - timedelta(days=3)
    remaining = []
    for t in todos:
        if t.get('deleted') and t.get('deleted_at'):
            try:
                deleted_at = datetime.fromisoformat(t.get('deleted_at'))
                if deleted_at < cutoff:
                    changed = True
                    continue
            except Exception:
                pass
        remaining.append(t)
    if changed:
        save_todos(remaining)
    return remaining

def validate_due_date(due):
    """Validate due date in mm/dd/yyyy format"""
    if not re.match(r'^(0[1-9]|1[0-2])/([0-2][0-9]|3[01])/\d{4}$', due):
        return False
    return True

def calculate_priority(due_date_str):
    """Calculate priority based on days until due date"""
    try:
        due_date = datetime.strptime(due_date_str, '%m/%d/%Y')
        today = datetime.today()
        days_remaining = (due_date - today).days
        
        if days_remaining < 0:
            return 'OVERDUE'
        elif days_remaining <= 3:
            return 'HIGH'
        elif days_remaining <= 7:
            return 'MEDIUM'
        else:
            return 'LOW'
    except ValueError:
        return 'N/A'

def get_priority_color(priority):
    """Return CSS class for priority color"""
    colors = {
        'OVERDUE': 'danger',
        'HIGH': 'warning',
        'MEDIUM': 'info',
        'LOW': 'success',
        'N/A': 'secondary'
    }
    return colors.get(priority, 'secondary')

# ============================================================================
# RECURRENCE AND NOTIFICATION FUNCTIONS
# ============================================================================

def parse_recurrence_pattern(pattern_str):
    """Parse recurrence pattern string. Format: 'daily|weekly|monthly|yearly|none'"""
    if not pattern_str or pattern_str == 'none':
        return None
    return pattern_str.lower()

def get_next_occurrence_date(due_date_str, pattern):
    """Calculate next occurrence date based on recurrence pattern"""
    if not pattern or pattern == 'none':
        return None
    try:
        current_due = datetime.strptime(due_date_str, '%m/%d/%Y')
        if pattern == 'daily':
            next_due = current_due + timedelta(days=1)
        elif pattern == 'weekly':
            next_due = current_due + timedelta(weeks=1)
        elif pattern == 'monthly':
            # Add approximately 30 days (basic month logic)
            if current_due.month == 12:
                next_due = current_due.replace(year=current_due.year + 1, month=1)
            else:
                next_due = current_due.replace(month=current_due.month + 1)
        elif pattern == 'yearly':
            next_due = current_due.replace(year=current_due.year + 1)
        else:
            return None
        return next_due.strftime('%m/%d/%Y')
    except Exception:
        return None

def check_and_handle_notifications(todos):
    """Check for priority changes and create notifications"""
    notifications = []
    for idx, todo in enumerate(todos, 1):
        if todo.get('deleted') or todo.get('saved'):
            continue
        current_priority = calculate_priority(todo.get('due', ''))
        previous_priority = todo.get('previous_priority', None)
        # If priority changed, log notification
        if previous_priority and previous_priority != current_priority:
            notifications.append({
                'type': 'priority_change',
                'task': todo.get('task'),
                'old_priority': previous_priority,
                'new_priority': current_priority,
                'timestamp': datetime.now().isoformat()
            })
        # Update previous priority for next check
        todo['previous_priority'] = current_priority
    return notifications

def get_high_priority_reminder(todos):
    """Get count and summary of high priority tasks for daily reminder"""
    high_priority_tasks = []
    for todo in todos:
        if not todo.get('completed') and not todo.get('deleted') and not todo.get('saved'):
            priority = calculate_priority(todo.get('due', ''))
            if priority in ['HIGH', 'OVERDUE']:
                high_priority_tasks.append({
                    'task': todo.get('task'),
                    'priority': priority,
                    'due': todo.get('due')
                })
    return high_priority_tasks

def handle_recurring_task_completion(todos, idx):
    """When a recurring task is marked complete, create next occurrence"""
    if idx < 1 or idx > len(todos):
        return
    todo = todos[idx - 1]
    pattern = todo.get('recurrence')
    if pattern and pattern != 'none':
        next_due = get_next_occurrence_date(todo.get('due', ''), pattern)
        if next_due:
            # Create a new task for next occurrence
            new_todo = {
                'task': todo.get('task'),
                'due': next_due,
                'description': todo.get('description', ''),
                'recurrence': pattern,
                'completed': False,
                'completed_at': None,
                'deleted': False,
                'deleted_at': None,
                'saved': False,
                'saved_at': None,
                'previous_priority': None
            }
            todos.append(new_todo)
            save_todos(todos)

# ============================================================================
# JINJA2 CONTEXT PROCESSOR - Make functions available in templates
# ============================================================================

@app.context_processor
def inject_template_functions():
    """Inject utility functions into Jinja2 template context"""
    return {
        'calculate_priority': calculate_priority,
        'get_priority_color': get_priority_color,
        'get_high_priority_reminder': get_high_priority_reminder
    }

# ============================================================================
# PWA ROUTES
# ============================================================================

@app.route('/manifest.json')
def manifest():
    """Serve PWA manifest for installation"""
    manifest_path = os.path.join(os.path.dirname(__file__), 'manifest.json')
    return send_file(manifest_path, mimetype='application/manifest+json')

@app.route('/service-worker.js')
def service_worker():
    """Serve service worker for offline support and caching"""
    sw_path = os.path.join(os.path.dirname(__file__), 'static', 'js', 'service-worker.js')
    return send_file(sw_path, mimetype='application/javascript')

# ============================================================================
# ROUTES
# ============================================================================

def sort_tasks(tasks, sort_by='alpha-asc'):
    """Sort tasks by different criteria"""
    if sort_by == 'alpha-asc':
        return sorted(tasks, key=lambda t: t.get('task', '').lower())
    elif sort_by == 'alpha-desc':
        return sorted(tasks, key=lambda t: t.get('task', '').lower(), reverse=True)
    elif sort_by == 'date-oldest':
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%m/%d/%Y')
            except:
                return datetime.max
        return sorted(tasks, key=lambda t: parse_date(t.get('due', '')))
    elif sort_by == 'date-newest':
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%m/%d/%Y')
            except:
                return datetime.max
        return sorted(tasks, key=lambda t: parse_date(t.get('due', '')), reverse=True)
    return tasks

@app.route('/')
def dashboard():
    """Main dashboard showing all tasks organized by status"""
    todos = cleanup_completed(load_todos())
    todos = cleanup_deleted(todos)
    # default to showing oldest due date first unless user overrides
    sort_by = request.args.get('sort', 'date-oldest')

    # Build active_todos from the full list so `idx` refers to the global todos index
    active_todos = []
    for i, t in enumerate(todos, 1):
        if not t.get('deleted', False) and not t.get('saved', False):
            t['idx'] = i
            t['priority'] = calculate_priority(t.get('due', ''))
            t['priority_color'] = get_priority_color(t['priority'])
            active_todos.append(t)

    # Filter by status from the active set
    pending = [t for t in active_todos if not t.get('completed', False)]
    completed = [t for t in active_todos if t.get('completed', False)]
    overdue = [t for t in active_todos if not t.get('completed', False) and t.get('priority') == 'OVERDUE']

    # Sort each section
    pending = sort_tasks(pending, sort_by)
    completed = sort_tasks(completed, sort_by)
    overdue = sort_tasks(overdue, sort_by)
    
    saved = [t for t in todos if t.get('saved', False) and not t.get('deleted', False)]
    deleted = [t for t in todos if t.get('deleted', False)]
    
    # Get high priority reminder
    high_priority_reminder = get_high_priority_reminder(todos)
    
    return render_template('dashboard.html', 
                         pending=pending,
                         completed=completed,
                         overdue=overdue,
                         saved_count=len(saved),
                         deleted_count=len(deleted),
                         total=len(active_todos),
                         sort_by=sort_by,
                         high_priority_reminder=high_priority_reminder,
                         high_priority_count=len(high_priority_reminder))



@app.route('/pending')
def pending_tasks():
    """View pending (incomplete) tasks"""
    todos = cleanup_completed(load_todos())
    todos = cleanup_deleted(todos)
    pending = []
    for idx, todo in enumerate(todos, 1):
        if not todo.get('completed', False) and not todo.get('deleted', False):
            todo['idx'] = idx
            todo['priority'] = calculate_priority(todo.get('due', ''))
            todo['priority_color'] = get_priority_color(todo['priority'])
            pending.append(todo)
    return render_template('pending.html', todos=pending)

@app.route('/completed')
def completed_tasks():
    """View completed tasks"""
    todos = cleanup_completed(load_todos())
    todos = cleanup_deleted(todos)
    completed = []
    for idx, todo in enumerate(todos, 1):
        if todo.get('completed', False) and not todo.get('deleted', False):
            todo['idx'] = idx
            todo['priority'] = calculate_priority(todo.get('due', ''))
            todo['priority_color'] = get_priority_color(todo['priority'])
            completed.append(todo)
    return render_template('completed.html', todos=completed)

@app.route('/deleted')
def deleted_tasks():
    """View deleted tasks"""
    todos = load_todos()
    deleted = []
    for idx, todo in enumerate(todos, 1):
        if todo.get('deleted', False):
            todo['idx'] = idx
            todo['priority'] = calculate_priority(todo.get('due', ''))
            todo['priority_color'] = get_priority_color(todo['priority'])
            if todo.get('deleted_at'):
                deleted_at = datetime.fromisoformat(todo['deleted_at'])
                days_deleted = (datetime.now() - deleted_at).days
                todo['days_until_permanent'] = max(0, 3 - days_deleted)
            deleted.append(todo)
    return render_template('deleted.html', todos=deleted)

@app.route('/overdue')
def overdue_tasks():
    """View overdue tasks"""
    todos = cleanup_completed(load_todos())
    todos = cleanup_deleted(todos)
    overdue = []
    for idx, todo in enumerate(todos, 1):
        if not todo.get('deleted', False) and not todo.get('saved', False):
            priority = calculate_priority(todo.get('due', ''))
            if priority == 'OVERDUE':
                todo['idx'] = idx
                todo['priority'] = priority
                todo['priority_color'] = get_priority_color(priority)
                overdue.append(todo)
    return render_template('overdue.html', todos=overdue)

@app.route('/saved')
def saved_tasks():
    """View saved/archived tasks"""
    todos = cleanup_completed(load_todos())
    todos = cleanup_deleted(todos)
    saved = []
    for idx, todo in enumerate(todos, 1):
        if todo.get('saved', False) and not todo.get('deleted', False):
            todo['idx'] = idx
            todo['priority'] = calculate_priority(todo.get('due', ''))
            todo['priority_color'] = get_priority_color(todo['priority'])
            saved.append(todo)
    return render_template('saved.html', todos=saved)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """Add a new task"""
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        due = request.form.get('due', '').strip()
        description = request.form.get('description', '').strip()
        recurrence = request.form.get('recurrence', 'none').strip()
        
        if not task:
            return render_template('add_task.html', error='Task name cannot be empty.'), 400
        
        if not validate_due_date(due):
            return render_template('add_task.html', error='Invalid date format. Use mm/dd/yyyy.'), 400
        
        todos = load_todos()
        todos.append({
            'task': task,
            'due': due,
            'description': description,
            'recurrence': recurrence,
            'completed': False,
            'completed_at': None,
            'deleted': False,
            'deleted_at': None,
            'saved': False,
            'saved_at': None,
            'previous_priority': None
        })
        save_todos(todos)
        return redirect(url_for('dashboard'))
    
    return render_template('add_task.html')

@app.route('/edit/<int:idx>', methods=['GET', 'POST'])
def edit_task(idx):
    """Edit an existing task"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        due = request.form.get('due', '').strip()
        description = request.form.get('description', '').strip()
        recurrence = request.form.get('recurrence', 'none').strip()
        
        if not task:
            todo = todos[idx - 1]
            return render_template('edit_task.html', idx=idx, todo=todo, error='Task name cannot be empty.'), 400
        
        if not validate_due_date(due):
            todo = todos[idx - 1]
            return render_template('edit_task.html', idx=idx, todo=todo, error='Invalid date format. Use mm/dd/yyyy.'), 400
        
        todos[idx - 1]['task'] = task
        todos[idx - 1]['due'] = due
        todos[idx - 1]['description'] = description
        todos[idx - 1]['recurrence'] = recurrence
        save_todos(todos)
        return redirect(url_for('dashboard'))
    
    todo = todos[idx - 1]
    return render_template('edit_task.html', idx=idx, todo=todo)

@app.route('/complete/<int:idx>', methods=['POST'])
def complete_task(idx):
    """Toggle task completion status - complete or uncomplete"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    # Toggle the completed status
    if todos[idx - 1].get('completed', False):
        # If already completed, mark as incomplete
        todos[idx - 1]['completed'] = False
        todos[idx - 1]['completed_at'] = None
    else:
        # If incomplete, mark as complete
        todos[idx - 1]['completed'] = True
        todos[idx - 1]['completed_at'] = datetime.now().isoformat()
        # If recurring, create next occurrence
        handle_recurring_task_completion(todos, idx)
    
    todos = cleanup_completed(todos)
    # Check for priority changes and store for notifications
    check_and_handle_notifications(todos)
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/delete/<int:idx>', methods=['POST'])
def delete_task(idx):
    """Soft delete a task - move to trash"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    # Mark as deleted instead of removing
    todos[idx - 1]['deleted'] = True
    todos[idx - 1]['deleted_at'] = datetime.now().isoformat()
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/restore/<int:idx>', methods=['POST'])
def restore_task(idx):
    """Restore a deleted task"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    if todos[idx - 1].get('deleted', False):
        todos[idx - 1]['deleted'] = False
        todos[idx - 1]['deleted_at'] = None
        save_todos(todos)
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 400

@app.route('/permanent-delete/<int:idx>', methods=['POST'])
def permanent_delete(idx):
    """Permanently delete a task"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    todos.pop(idx - 1)
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/save/<int:idx>', methods=['POST'])
def save_task(idx):
    """Save/archive a completed task"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    todos[idx - 1]['saved'] = True
    todos[idx - 1]['saved_at'] = datetime.now().isoformat()
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/unsave/<int:idx>', methods=['POST'])
def unsave_task(idx):
    """Unsave/unarchive a task"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    if todos[idx - 1].get('saved', False):
        todos[idx - 1]['saved'] = False
        todos[idx - 1]['saved_at'] = None
        save_todos(todos)
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 400

@app.route('/api/task/<int:idx>')
def get_task_details(idx):
    """Get task details for modal display"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    todo = todos[idx - 1]
    return jsonify({
        'success': True,
        'task': todo.get('task', ''),
        'description': todo.get('description', ''),
        'due': todo.get('due', 'N/A'),
        'priority': calculate_priority(todo.get('due', '')),
        'completed': todo.get('completed', False),
        'deleted': todo.get('deleted', False),
        'saved': todo.get('saved', False)
    })

@app.route('/search')
def search():
    """Search tasks across all statuses"""
    query = request.args.get('q', '').strip().lower()
    todos = load_todos()
    
    if not query:
        matches = []
    else:
        matches = []
        for idx, todo in enumerate(todos, 1):
            if query in todo.get('task', '').lower() or query in todo.get('description', '').lower():
                todo['idx'] = idx
                todo['priority'] = calculate_priority(todo.get('due', ''))
                todo['priority_color'] = get_priority_color(todo['priority'])
                matches.append(todo)
    
    return render_template('search.html', query=query, matches=matches)

@app.route('/api/bulk-action', methods=['POST'])
def bulk_action():
    """Handle bulk actions on multiple tasks"""
    data = request.get_json()
    action = data.get('action')
    indices = data.get('indices', [])
    
    todos = load_todos()
    
    if not indices or not action:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400
    
    # Sort indices in reverse to delete from end first (avoid index shifting)
    sorted_indices = sorted([int(i) for i in indices], reverse=True)
    
    if action == 'delete':
        for idx in sorted_indices:
            if 1 <= idx <= len(todos):
                todos.pop(idx - 1)
    elif action == 'complete':
        for idx in sorted_indices:
            if 1 <= idx <= len(todos):
                todos[idx - 1]['completed'] = True
                todos[idx - 1]['completed_at'] = datetime.now().isoformat()
    
    todos = cleanup_completed(todos)
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/api/stats')
def get_stats():
    """API endpoint for stats"""
    todos = cleanup_completed(load_todos())
    total = len(todos)
    completed = sum(1 for t in todos if t.get('completed', False))
    incomplete = total - completed
    overdue = sum(1 for t in todos if not t.get('completed') and calculate_priority(t.get('due', '')) == 'OVERDUE')
    
    return jsonify({
        'total': total,
        'completed': completed,
        'incomplete': incomplete,
        'overdue': overdue
    })

@app.route('/api/daily-reminder')
def daily_reminder():
    """Get daily reminder of high priority tasks"""
    todos = cleanup_completed(load_todos())
    todos = cleanup_deleted(todos)
    high_priority = get_high_priority_reminder(todos)
    
    return jsonify({
        'success': True,
        'count': len(high_priority),
        'tasks': high_priority,
        'message': f"You have {len(high_priority)} high priority tasks pending" if high_priority else "No high priority tasks today!"
    })

@app.route('/api/task-notifications/<int:idx>')
def get_task_notifications(idx):
    """Get notifications for a specific task (priority changes)"""
    todos = load_todos()
    if idx < 1 or idx > len(todos):
        return jsonify({'success': False}), 400
    
    todo = todos[idx - 1]
    current_priority = calculate_priority(todo.get('due', ''))
    previous_priority = todo.get('previous_priority')
    
    notifications = []
    if previous_priority and previous_priority != current_priority:
        notifications.append({
            'message': f"{todo.get('task')} moved to {current_priority}",
            'old_priority': previous_priority,
            'new_priority': current_priority,
            'type': 'priority_change'
        })
    
    return jsonify({
        'success': True,
        'notifications': notifications,
        'current_priority': current_priority
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
 