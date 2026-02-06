import json
import os
import argparse
import re
from datetime import datetime, timedelta

TODO_FILE = 'todos.json'

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print('Error: Could not read todos.json. Starting with an empty list.')
        return []

def save_todos(todos):
    try:
        with open(TODO_FILE, 'w') as f:
            json.dump(todos, f, indent=2)
    except IOError:
        print('Error: Could not save todos.')


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
                # if parsing fails, keep the item
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
    """Calculate priority (high/medium/low) based on days until due date"""
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

def list_todos(todos, show_incomplete_only=False):
    """Display todos with priority indicators"""
    if not todos:
        print('\n  ℹ  No todos found.')
        return
    
    # Determine which items to display; keep original indices for commands
    display_any = False
    
    print('\n' + '='*70)
    print('  CURRENT TASKS')
    print('='*70)
    for idx, todo in enumerate(todos, 1):
        if show_incomplete_only and todo.get('completed', False):
            continue
        display_any = True
        status = '✓' if todo.get('completed', False) else '○'
        priority = calculate_priority(todo.get('due', ''))
        due = todo.get('due', 'N/A')
        task = todo['task']

        # Color/format priority
        priority_str = f'[{priority}]'

        # Format with strikethrough for completed
        if todo.get('completed', False):
            task = f'~~{task}~~'

        print(f"  {idx}. [{status}] {task:40} | {due:10} | {priority_str:11}")
        # Optional description on next line
        desc = todo.get('description', '').strip()
        if desc:
            print(f"      → {desc}")

    if not display_any:
        print('\n  ✓ All tasks completed!')

    print('='*70 + '\n')

def add_todo(todos, task, due, description=''):
    """Add a new todo with task and due date"""
    if not validate_due_date(due):
        print('  ✗ Error: Due date must be in mm/dd/yyyy format.')
        return False
    todos.append({'task': task, 'due': due, 'completed': False, 'description': description, 'completed_at': None})
    save_todos(todos)
    priority = calculate_priority(due)
    print(f'  ✓ Added: "{task}" (Due: {due}) - Priority: [{priority}]')
    return True

def delete_todo(todos, idx):
    """Delete a todo by index"""
    if idx < 1 or idx > len(todos):
        print('  ✗ Error: Invalid task number.')
        return False
    removed = todos.pop(idx - 1)
    save_todos(todos)
    print(f'  ✓ Deleted: "{removed["task"]}"')
    return True

def complete_todo(todos, idx):
    """Mark a todo as completed"""
    if idx < 1 or idx > len(todos):
        print('  ✗ Error: Invalid task number.')
        return False
    todos[idx - 1]['completed'] = True
    todos[idx - 1]['completed_at'] = datetime.now().isoformat()
    save_todos(todos)
    print(f'  ✓ Completed: "{todos[idx - 1]["task"]}"')
    # Cleanup any old completed tasks and update the list in-place
    remaining = cleanup_completed(todos)
    todos.clear()
    todos.extend(remaining)
    return todos

def edit_todo(todos, idx):
    """Edit task name, description, or due date interactively by index."""
    if idx < 1 or idx > len(todos):
        print('  ✗ Error: Invalid task number.')
        return False
    todo = todos[idx - 1]
    print('\n  EDIT TASK')
    print('  Leave input blank to keep current value.')
    new_name = input(f'  New name [{todo.get("task")}]: ').strip()
    if new_name:
        todo['task'] = new_name

    new_desc = input(f'  New description [{todo.get("description","")}]: ').strip()
    if new_desc != '':
        todo['description'] = new_desc

    while True:
        new_due = input(f'  New due date (mm/dd/yyyy) [{todo.get("due")}]: ').strip()
        if not new_due:
            break
        if validate_due_date(new_due):
            todo['due'] = new_due
            break
        print('  ✗ Invalid format. Please use mm/dd/yyyy')

    save_todos(todos)
    print(f'  ✓ Updated task #{idx}: "{todo.get("task")}"')
    return True

def search_todos(todos, query):
    """Search tasks by name or description and display matches with global indices."""
    q = query.strip().lower()
    if not q:
        print('  ✗ Provide a search term.')
        return
    matches = []
    for idx, t in enumerate(todos, 1):
        if q in t.get('task','').lower() or q in t.get('description','').lower():
            matches.append((idx, t))

    if not matches:
        print('  ℹ  No matches found.')
        return

    print('\n' + '-'*60)
    print(f'  SEARCH RESULTS for "{query}"')
    print('-'*60)
    for idx, todo in matches:
        status = '✓' if todo.get('completed') else '○'
        priority = calculate_priority(todo.get('due',''))
        due = todo.get('due','N/A')
        print(f"  {idx}. [{status}] {todo.get('task') :40} | {due:10} | [{priority}]")
        desc = todo.get('description','').strip()
        if desc:
            print(f"      → {desc}")
    print('-'*60 + '\n')

def display_menu():
    """Display main menu options"""
    print('\n' + '='*70)
    print('  WHAT WOULD YOU LIKE TO DO?')
    print('='*70)
    print('  1. add [a]           - Add a new task')
    print('  2. list [l]          - View all tasks')
    print('  3. complete [c] <#>  - Mark task as done')
    print('  4. delete [d] <#>    - Remove a task')
    print('  5. edit [e] <#>      - Edit a task (name/description/due)')
    print('  6. search [s] <term> - Search tasks by keyword')
    print('  7. quit [q]          - Exit application')
    print('='*70 + '\n')

def interactive_add(todos):
    """Interactive mode for adding a todo with separate prompts"""
    print('\n' + '-'*70)
    print('  ADD NEW TASK')
    print('-'*70)
    
    task = input('  Enter task name: ').strip()
    if not task:
        print('  ✗ Task cannot be empty.')
        return False
    
    # Optional description
    description = input('  (Optional) Enter task description (press Enter to skip): ').strip()

    while True:
        due = input('  Enter due date (mm/dd/yyyy): ').strip()
        if validate_due_date(due):
            break
        print('  ✗ Invalid format. Please use mm/dd/yyyy (e.g., 02/14/2026)')
    
    return add_todo(todos, task, due, description)

def main():
    parser = argparse.ArgumentParser(description='Todo List App - Stay Organized & On Time')
    parser.add_argument('command', nargs='?', help='Command: add/list/delete/complete/quit')
    parser.add_argument('arg', nargs='*', help='Additional arguments')
    args = parser.parse_args()

    todos = load_todos()
    # Remove completed tasks older than 2 days on startup
    todos = cleanup_completed(todos)

    # Command-line mode
    if args.command:
        cmd = args.command.lower()
        if cmd in ('add', 'a') and len(args.arg) >= 2:
            *task_parts, due = args.arg
            add_todo(todos, ' '.join(task_parts), due, '')
        elif cmd in ('list', 'l'):
            list_todos(todos)
        elif cmd in ('delete', 'd') and args.arg and args.arg[0].isdigit():
            delete_todo(todos, int(args.arg[0]))
        elif cmd in ('complete', 'c') and args.arg and args.arg[0].isdigit():
            complete_todo(todos, int(args.arg[0]))
        elif cmd in ('edit', 'e') and args.arg and args.arg[0].isdigit():
            edit_todo(todos, int(args.arg[0]))
        elif cmd in ('search', 's') and args.arg:
            search_todos(todos, ' '.join(args.arg))
        elif cmd in ('quit', 'q'):
            print('  Goodbye!')
        else:
            print('  ✗ Invalid command or missing argument.')
        return

    # Interactive mode
    print('\n' + '='*70)
    print('  WELCOME TO TODO APP')
    print('  Your Personal Task Manager for Organization & Punctuality')
    print('='*70)
    
    # Show current tasks on startup
    if todos:
        list_todos(todos)
    
    while True:
        display_menu()
        inp = input('  Enter command: ').strip().lower()
        
        if not inp:
            continue
        
        parts = inp.split()
        cmd = parts[0]
        
        # Flexible input handling
        if cmd in ('add', 'a'):
            interactive_add(todos)
        elif cmd in ('list', 'l'):
            list_todos(todos)
        elif cmd in ('complete', 'c', 'done', 'finish'):
            if len(parts) > 1 and parts[1].isdigit():
                complete_todo(todos, int(parts[1]))
            else:
                print('  ✗ Usage: complete <task number>')
        elif cmd in ('delete', 'd', 'remove', 'rm'):
            if len(parts) > 1 and parts[1].isdigit():
                delete_todo(todos, int(parts[1]))
            else:
                print('  ✗ Usage: delete <task number>')
        elif cmd in ('edit', 'e'):
            if len(parts) > 1 and parts[1].isdigit():
                edit_todo(todos, int(parts[1]))
            else:
                print('  ✗ Usage: edit <task number>')
        elif cmd in ('search', 's'):
            if len(parts) > 1:
                search_todos(todos, ' '.join(parts[1:]))
            else:
                print('  ✗ Usage: search <term>')
        elif cmd in ('quit', 'q', 'exit', 'bye'):
            print('  Goodbye! Stay organized and punctual! ✓')
            break
        else:
            print('  ✗ Unknown command. Please try again.')

def run():
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n  Exiting. Goodbye!')

if __name__ == '__main__':
    run()
