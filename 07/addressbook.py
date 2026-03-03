
from collections import UserDict
from datetime import datetime, timedelta


class Birthday:
    """Клас для зберігання дня народження контакту."""

    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону контакту з валідацією."""

    def __init__(self, value: str):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Телефонний номер має складатися з 10 цифр.")
        super().__init__(value)


class Record:
    """Клас для представлення запису контакту в адресній книзі."""

    def __init__(self, name: Name):
        self.name = name
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: Phone) -> None:
        """Додає новий телефон до запису."""
        self.phones.append(phone)

    def remove_phone(self, phone: Phone) -> None:
        """Видаляє телефон із запису, якщо такий існує."""
        self.phones = [p for p in self.phones if p.value != phone.value]

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        """Редагує існуючий номер телефону, замінюючи його на новий."""
        for idx, p in enumerate(self.phones):
            if p.value == old_phone.value:
                self.phones[idx] = new_phone
                break

    def find_phone(self, phone: Phone) -> Phone | None:
        """Повертає телефон із запису, якщо він є."""
        for p in self.phones:
            if p.value == phone.value:
                return p
        return None

    def add_birthday(self, birthday_str: str) -> None:
        """Додає або оновлює день народження для контакту."""
        self.birthday = Birthday(birthday_str)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "нема телефонів"
        birthday_str = str(self.birthday) if self.birthday else "не вказано"
        return f"Контакт {self.name.value}, телефони: {phones_str}, день народження: {birthday_str}"


class AddressBook(UserDict):
    """Клас адресної книги, що зберігає всі записи контактів."""

    def add_record(self, record: Record) -> None:
        """Додає новий запис у книгу."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Повертає запис за ім'ям, якщо він існує."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за ім'ям, якщо він існує."""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7) -> list[Record]:
        """Повертає записи з днями народження у найближчі 'days' днів."""
        today = datetime.today().date()
        end_date = today + timedelta(days=days)
        result: list[Record] = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.value
            this_year_bday = bday.replace(year=today.year)

            if this_year_bday < today:
                this_year_bday = this_year_bday.replace(year=today.year + 1)

            if today <= this_year_bday <= end_date:
                result.append(record)

        return result
