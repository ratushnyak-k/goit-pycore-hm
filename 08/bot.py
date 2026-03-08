from addressbook import AddressBook, Record, Name, Phone, save_data, load_data


def add_contact(args, contacts: AddressBook) -> str:
    if len(args) < 2:
        return "Вкажи ім'я та номер телефону."
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
    return f"Контакт {name} з номером {phone} додано."


def change_phone(args, contacts: AddressBook) -> str:
    if len(args) < 3:
        return "Вкажи ім'я, старий і новий номер телефону."
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = contacts.find(name)
    if record is None:
        return "Контакт не знайдено."
    try:
        old_phone_obj = Phone(old_phone)
        new_phone_obj = Phone(new_phone)
    except ValueError as e:
        return str(e)
    if record.find_phone(old_phone_obj) is None:
        return "Старий номер не знайдено."
    record.edit_phone(old_phone_obj, new_phone_obj)
    return f"Номер {old_phone} змінено на {new_phone} для контакту {name}."


def get_phone(args, contacts: AddressBook) -> str:
    if len(args) < 1:
        return "Вкажи ім'я контакту."
    name = args[0]
    record = contacts.find(name)
    if record is None:
        return "Контакт не знайдено."
    if not record.phones:
        return "Номерів не знайдено."
    phones = ", ".join(phone.value for phone in record.phones)
    return f"{name}: {phones}"


def add_birthday_command(args, contacts: AddressBook) -> str:
    if len(args) < 2:
        return "Вкажи ім'я та дату народження у форматі DD.MM.YYYY."
    name, birthday_str = args[0], args[1]
    record = contacts.find(name)
    if not record:
        return "Контакт не знайдено."
    try:
        record.add_birthday(birthday_str)
    except ValueError as e:
        return str(e)
    return f"День народження {birthday_str} додано для контакту {name}."


def show_birthday_command(args, contacts: AddressBook) -> str:
    if len(args) < 1:
        return "Вкажи ім'я контакту."
    name = args[0]
    record = contacts.find(name)
    if not record:
        return "Контакт не знайдено."
    if not record.birthday:
        return "День народження не вказано."
    return f"{name}: {record.birthday}"


def birthdays_command(args, contacts: AddressBook) -> str:
    upcoming = contacts.get_upcoming_birthdays()
    if not upcoming:
        return "Найближчі 7 днів немає днів народження."
    lines = []
    for record in upcoming:
        lines.append(f"{record.name.value}: {record.birthday}")
    return "\n".join(lines)


def show_all(args, contacts: AddressBook) -> str:
    if not contacts.data:
        return "Адресна книга порожня."
    lines = []
    for record in contacts.data.values():
        lines.append(str(record))
    return "\n".join(lines)


def parse_input(user_input: str):
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args


def main():
    contacts = load_data()
    print("Ласкаво просимо! Введи 'help' для списку команд.")

    while True:
        user_input = input(">>> ")
        command, args = parse_input(user_input)

        if command in ("close", "exit", "quit"):
            save_data(contacts)
            print("Адресну книгу збережено. До побачення!")
            break
        elif command == "hello":
            result = "Привіт! Чим можу допомогти?"
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
                "  hello                             — привітання\n"
                "  add <ім'я> <телефон>              — додати контакт\n"
                "  change <ім'я> <старий> <новий>    — змінити номер\n"
                "  phone <ім'я>                      — показати номер\n"
                "  add-birthday <ім'я> <DD.MM.YYYY>  — додати день народження\n"
                "  show-birthday <ім'я>              — показати день народження\n"
                "  birthdays                         — дні народження за 7 днів\n"
                "  all                               — всі контакти\n"
                "  close / exit / quit               — зберегти і вийти"
            )
        else:
            result = "Невідома команда. Введи 'help' для списку команд."

        print(result)


if __name__ == "__main__":
    main()
