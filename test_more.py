import requests
import json
import time
import shutil

BASE = 'http://127.0.0.1:5000'

BACKUP = 'todos.bak.json'

def load_todos():
    with open('todos.json','r') as f:
        return json.load(f)

def save_todos_local(todos):
    with open('todos.json','w') as f:
        json.dump(todos, f, indent=2)


def find_active_indices(todos, max_count=3):
    res = []
    for i, t in enumerate(todos, 1):
        if not t.get('deleted', False) and not t.get('saved', False):
            res.append(i)
            if len(res) >= max_count:
                break
    return res


def main():
    # backup
    shutil.copyfile('todos.json', BACKUP)
    print('Backup created')

    todos = load_todos()
    indices = find_active_indices(todos, max_count=3)
    if not indices:
        print('No active tasks to test')
        return
    idx = indices[0]
    print('Using index', idx)

    # Toggle complete
    r = requests.post(f'{BASE}/complete/{idx}')
    print('/complete status', r.status_code)
    time.sleep(0.2)
    todos = load_todos()
    print('completed after toggle:', todos[idx-1].get('completed'))

    # Toggle back
    r = requests.post(f'{BASE}/complete/{idx}')
    print('/complete undo status', r.status_code)
    time.sleep(0.2)
    todos = load_todos()
    print('completed after undo:', todos[idx-1].get('completed'))

    # Ensure completed then save
    r = requests.post(f'{BASE}/complete/{idx}')
    time.sleep(0.1)
    r = requests.post(f'{BASE}/save/{idx}')
    print('/save status', r.status_code)
    time.sleep(0.2)
    todos = load_todos()
    print('saved flag:', todos[idx-1].get('saved'))

    # Unsave
    r = requests.post(f'{BASE}/unsave/{idx}')
    print('/unsave status', r.status_code)
    time.sleep(0.2)
    todos = load_todos()
    print('saved after unsave:', todos[idx-1].get('saved'))

    # Bulk complete on up to 3 indices
    if len(indices) > 1:
        payload = {'action': 'complete', 'indices': indices}
        r = requests.post(f'{BASE}/api/bulk-action', json=payload)
        print('/api/bulk-action status', r.status_code)
        time.sleep(0.2)
        todos = load_todos()
        print('bulk completed flags:', [todos[i-1].get('completed') for i in indices])

    # restore backup to avoid side-effects
    shutil.copyfile(BACKUP, 'todos.json')
    print('Restored backup')

if __name__ == '__main__':
    main()
