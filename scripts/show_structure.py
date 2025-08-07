import os
from dotenv import load_dotenv

IGNORED_DIRS = {'__pycache__', '.git', '.venv', 'env', 'venv', 'migrations'}

def print_tree(start_path, prefix=''):
    items = sorted(os.listdir(start_path))
    for index, item in enumerate(items):
        if item in IGNORED_DIRS:
            continue
        path = os.path.join(start_path, item)
        connector = '└── ' if index == len(items) - 1 else '├── '
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = '    ' if index == len(items) - 1 else '│   '
            print_tree(path, prefix + extension)

def main():
    print("Структура проекта:\n")
    print_tree('.')  # Корневая папка

    print("\nЗагрузка .env ...")
    load_dotenv()
    db_url = os.getenv("DB_URL")

    if db_url:
        print(f"\n🔗 Строка подключения к БД (DB_URL): {db_url}")
    else:
        print("⚠️ Переменная окружения DB_URL не найдена в .env")

if __name__ == "__main__":
    main()