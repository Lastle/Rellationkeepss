import os

EXCLUDED_DIRS = {
    '.git', '.idea', '.vscode', '__pycache__',
    'venv', '.venv', 'env', 'migrations',
    '.pytest_cache', '.mypy_cache', '.ruff_cache',
    '.tox', '.egg-info', '.cache', 'dist', 'build'
}

EXCLUDED_FILES = {
    '__init__.pyc', '__pycache__'
}

def print_tree(path='.', prefix=''):
    entries = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            if item not in EXCLUDED_DIRS:
                entries.append((item, True))
        elif item.endswith('.py') and item not in EXCLUDED_FILES:
            entries.append((item, False))

    entries.sort()
    for idx, (name, is_dir) in enumerate(entries):
        connector = '└── ' if idx == len(entries) - 1 else '├── '
        print(prefix + connector + name)
        if is_dir:
            new_prefix = prefix + ('    ' if idx == len(entries) - 1 else '│   ')
            print_tree(os.path.join(path, name), new_prefix)

if __name__ == '__main__':
    print_tree()
