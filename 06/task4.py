def parse_input(user_input):
    """Розбиває рядок на команду та аргументи."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


def add_contact(args, contacts):
    """Додає новий контакт. Очікує: ім'я та телефон."""
    if len(args) < 2:
        return "Введіть ім'я та номер телефону."
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Contact added."


def change_contact(args, contacts):
    """Змінює номер телефону існуючого контакту."""
    if len(args) < 2:
        return "Введіть ім'я та новий номер телефону."
    name, phone = args[0], args[1]
    if name not in contacts:
        return f"Контакт '{name}' не знайдено."
    contacts[name] = phone
    return "Contact updated."


def show_phone(args, contacts):
    """Виводить номер телефону для вказаного імені."""
    if len(args) < 1:
        return "Введіть ім'я контакту."
    name = args[0]
    if name not in contacts:
        return f"Контакт '{name}' не знайдено."
    return contacts[name]


def show_all(contacts):
    """Виводить усі збережені контакти."""
    if not contacts:
        return "Контактів немає."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
