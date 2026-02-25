import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)


def visualize_directory(path: Path, indent: str = ""):
    """
    Рекурсивно виводить структуру директорії.
    Директорії — синім, файли — зеленим.
    """
    try:
        items = sorted(path.iterdir())
    except PermissionError:
        print(f"{indent}{Fore.RED}[Немає доступу]{Style.RESET_ALL}")
        return

    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "└── " if is_last else "├── "
        new_indent = indent + ("    " if is_last else "│   ")

        if item.is_dir():
            print(f"{indent}{connector}{Fore.BLUE}{item.name}/{Style.RESET_ALL}")
            visualize_directory(item, new_indent)
        else:
            print(f"{indent}{connector}{Fore.GREEN}{item.name}{Style.RESET_ALL}")


def main():
    if len(sys.argv) < 2:
        print("Використання: python task3.py <шлях до директорії>")
        sys.exit(1)

    dir_path = Path(sys.argv[1])

    if not dir_path.exists():
        print(f"Помилка: шлях '{dir_path}' не існує.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Помилка: '{dir_path}' не є директорією.")
        sys.exit(1)

    print(f"{Fore.BLUE}{dir_path.name}/{Style.RESET_ALL}")
    visualize_directory(dir_path)


if __name__ == "__main__":
    main()
