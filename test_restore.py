import requests
import json
import time

BASE = 'http://127.0.0.1:5000'

def load_todos():
    with open('todos.json','r') as f:
        return json.load(f)


def find_first_active(todos):
    for i, t in enumerate(todos, 1):
        if not t.get('deleted', False) and not t.get('saved', False):
            return i, t
    return None, None


def main():
    todos = load_todos()
    idx, todo = find_first_active(todos)
    if not idx:
        print('No active task found in todos.json to test with.')
        return
    print('Testing task index', idx, 'title:', todo.get('task'))

    # Delete
    r = requests.post(f'{BASE}/delete/{idx}')
    print('Delete status:', r.status_code)
    time.sleep(0.5)
    todos = load_todos()
    print('Deleted flag after delete:', todos[idx-1].get('deleted'))

    # Restore
    r = requests.post(f'{BASE}/restore/{idx}')
    print('Restore status:', r.status_code)
    time.sleep(0.5)
    todos = load_todos()
    print('Deleted flag after restore:', todos[idx-1].get('deleted'))

if __name__ == '__main__':
    main()
