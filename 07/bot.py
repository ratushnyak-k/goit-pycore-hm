
from addressbook import AddressBook, Record, Name, Phone


def add_contact(args, contacts: AddressBook) -> str:
    """Додає новий контакт або телефон до існуючого контакту."""
    if len(args) < 2:
        return "Введіть ім'я та номер телефону."

    name, phone = args[0], args[1]
    record = contacts.find(name)

    if record is None:
        record = Record(Name(name))
        contacts.add_record(record)

    try:
        phone_obj = Phone(phone)
    except ValueError as e:
        return str(e)

    record.add_phone(phone_obj)
    return f"Контакт {name} з телефоном {phone} додано/оновлено."


def change_phone(args, contacts: AddressBook) -> str:
    """Змінює існуючий номер телефону контакту."""
    if len(args) < 3:
        return "Введіть ім'я, старий та новий номер телефону."

    name, old_phone, new_phone = args[0], args[1], args[2]
    record = contacts.find(name)

    if record is None:
        return "Контакт з таким ім'ям не знайдено."

    try:
        old_phone_obj = Phone(old_phone)
        new_phone_obj = Phone(new_phone)
    except ValueError as e:
        return str(e)

    if record.find_phone(old_phone_obj) is None:
        return "Старий номер телефону не знайдено у контакту."

    record.edit_phone(old_phone_obj, new_phone_obj)
    return f"Для контакту {name} змінено номер {old_phone} на {new_phone}."


def get_phone(args, contacts: AddressBook) -> str:
    """Повертає всі телефони контакту."""
    if len(args) < 1:
        return "Введіть ім'я контакту."

    name = args[0]
    record = contacts.find(name)

    if record is None:
        return "Контакт з таким ім'ям не знайдено."

    if not record.phones:
        return "У цього контакту немає збережених телефонів."

    phones = "; ".join(phone.value for phone in record.phones)
    return f"Телефони контакту {name}: {phones}."


def add_birthday_command(args, contacts: AddressBook) -> str:
    """Додає день народження контакту."""
    if len(args) < 2:
        return "Введіть ім'я та день народження у форматі DD.MM.YYYY."

    name, birthday_str = args[0], args[1]
    record = contacts.find(name)
    if not record:
        return "Контакт з таким ім'ям не знайдено."

    try:
        record.add_birthday(birthday_str)
    except ValueError as e:
        return str(e)

    return f"Для контакту {name} додано день народження {birthday_str}."


def show_birthday_command(args, contacts: AddressBook) -> str:
    """Показує день народження контакту."""
    if len(args) < 1:
        return "Введіть ім'я контакту."

    name = args[0]
    record = contacts.find(name)
    if not record:
        return "Контакт з таким ім'ям не знайдено."

    if not record.birthday:
        return "Для цього контакту день народження не вказано."

    return f"День народження контакту {name}: {record.birthday}."


def birthdays_command(args, contacts: AddressBook) -> str:
    """Показує контакти з днями народження у найближчі 7 днів."""
    upcoming = contacts.get_upcoming_birthdays()
    if not upcoming:
        return "Немає контактів з днями народження у найближчі 7 днів."

    lines = []
    for record in upcoming:
        lines.append(f"{record.name.value}: {record.birthday}")

    return "".join(lines)


def show_all(args, contacts: AddressBook) -> str:
    """Показує всі контакти в адресній книзі."""
    if not contacts.data:
        return "Адресна книга порожня."

    lines = []
    for record in contacts.data.values():
        lines.append(str(record))
    return "".join(lines)

def parse_input(user_input: str):
    """Парсить введений користувачем рядок на команду та аргументи."""
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args


def main():
    """Основна функція роботи бота з адресною книгою."""
    contacts = AddressBook()
    print("Вітаю! Я бот-довідник. Введіть 'help' для списку команд.")

    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit", "quit"):
            print("До побачення!")
            break
        elif command == "hello":
            result = "Чим я можу допомогти?"
        elif command == "add":
            result = add_contact(args, contacts)
        elif command == "change":
            result = change_phone(args, contacts)
        elif command == "phone":
            result = get_phone(args, contacts)
        elif command == "all":
            result = show_all(args, contacts)
        elif command == "add-birthday":
            result = add_birthday_command(args, contacts)
        elif command == "show-birthday":
            result = show_birthday_command(args, contacts)
        elif command == "birthdays":
            result = birthdays_command(args, contacts)
        elif command == "help":
            result = (
                "Доступні команди:\n"
                "  hello - привітання\n"
                "  add <name> <phone> - додати контакт або номер\n"
                "  change <name> <old_phone> <new_phone> - змінити номер\n"
                "  phone <name> - показати телефони контакту\n"
                "  add-birthday <name> <DD.MM.YYYY> - додати день народження\n"
                "  show-birthday <name> - показати день народження контакту\n"
                "  birthdays - дні народження на найближчі 7 днів\n"
                "  all - показати всі контакти\n"
                "  close/exit/quit - вийти з програми"
            )

        elif command == "":
            result = "Введіть, будь ласка, команду."
        else:
            result = "Невідома команда. Спробуйте ще раз або введіть 'help'."

        print(result)


if __name__ == "__main__":
    main()
