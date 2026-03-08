import pickle
from collections import UserDict
from datetime import datetime, timedelta


class Birthday:
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуй DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону має містити рівно 10 цифр")
        super().__init__(value)


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: Phone) -> None:
        self.phones.append(phone)

    def remove_phone(self, phone: Phone) -> None:
        self.phones = [p for p in self.phones if p.value != phone.value]

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        for idx, p in enumerate(self.phones):
            if p.value == old_phone.value:
                self.phones[idx] = new_phone
                break

    def find_phone(self, phone: Phone) -> Phone | None:
        for p in self.phones:
            if p.value == phone.value:
                return p
        return None

    def add_birthday(self, birthday_str: str) -> None:
        self.birthday = Birthday(birthday_str)

    def __str__(self) -> str:
        phones_str = ", ".join(p.value for p in self.phones) if self.phones else "немає"
        birthday_str = str(self.birthday) if self.birthday else "не вказано"
        return f"{self.name.value} | тел: {phones_str} | день народження: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7) -> list[Record]:
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


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """Зберігає адресну книгу у бінарний файл через pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """Завантажує адресну книгу з файлу. Якщо файл не існує — повертає нову книгу."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
