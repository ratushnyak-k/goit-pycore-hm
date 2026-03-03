from typing import Dict, Callable, Tuple

def input_error(func: Callable) -> Callable:
    """
    Декоратор перехоплює типові помилки (KeyError, ValueError, IndexError)
    та повертає користувачеві зрозуміле повідомлення, не перериваючи програму.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Користувача з таким ім'ям не знайдено."
        except ValueError:
            return "Дайте, будь ласка, ім'я та телефон через пробіл."
        except IndexError:
            return "Недостатньо аргументів для команди."

    return inner

def parse_command(user_input: str) -> Tuple[str, list]:
    """
    Розбиває введений рядок на команду та аргументи.
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


@input_error
def add_contact(args: list, contacts: Dict[str, str]) -> str:
    """
    Додає новий контакт у словник contacts.
    Очікує два аргументи: ім'я та телефон.
    """
    name, phone = args
    contacts[name] = phone
    return "Контакт додано."


@input_error
def change_contact(args: list, contacts: Dict[str, str]) -> str:
    """
    Змінює телефон існуючого контакта.
    Очікує два аргументи: ім'я та новий телефон.
    """
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Номер контакту оновлено."


@input_error
def get_phone(args: list, contacts: Dict[str, str]) -> str:
    """
    Повертає телефон контакта за ім'ям.
    Очікує один аргумент: ім'я.
    """
    name = args[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]


@input_error
def show_all(args: list, contacts: Dict[str, str]) -> str:
    """
    Повертає рядок з усіма контактами.
    """
    if not contacts:
        return "Список контактів порожній."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "".join(lines)


def main():
    """
    Основна функція бота-помічника.
    """
    contacts: Dict[str, str] = {}
    print("Вітаю! Це бот-помічник. Введіть команду.")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_command(user_input)

        if command in ("exit", "close", "good_bye", "bye"):
            print("До побачення!")
            break

        if command == "add":
            result = add_contact(args, contacts)
        elif command == "change":
            result = change_contact(args, contacts)
        elif command == "phone":
            result = get_phone(args, contacts)
        elif command == "all":
            result = show_all(args, contacts)
        elif command == "":
            result = "Введіть, будь ласка, команду."
        else:
            result = "Невідома команда. Спробуйте ще раз."

        print(result)


if __name__ == "__main__":
    main()
