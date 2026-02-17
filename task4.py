from datetime import datetime, timedelta, date


def get_upcoming_birthdays(users: list[dict]) -> list[dict]:
    """
    Повертає список словників з ключами:
    - 'name' — ім'я користувача
    - 'congratulation_date' — дата привітання у форматі 'YYYY.MM.DD'
    для тих, у кого день народження впродовж наступних 7 днів (включно).
    Якщо ДН на вихідні — переносимо на понеділок.
    """
    today = datetime.today().date()
    upcoming_limit = today + timedelta(days=7)
    result: list[dict] = []

    for user in users:
        name = user.get("name")
        birthday_str = user.get("birthday")

        if not name or not birthday_str:
            continue

        try:
            birthday_date = datetime.strptime(birthday_str, "%Y.%m.%d").date()
        except ValueError:
            continue

        birthday_this_year = birthday_date.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if not (today <= birthday_this_year <= upcoming_limit):
            continue

        congratulation_day = birthday_this_year

        if congratulation_day.weekday() == 5:
            congratulation_day += timedelta(days=2)
        elif congratulation_day.weekday() == 6:
            congratulation_day += timedelta(days=1)

        result.append(
            {
                "name": name,
                "congratulation_date": congratulation_day.strftime("%Y.%m.%d"),
            }
        )

    return result


if __name__ == "__main__":
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
        {"name": "John Smith", "birthday": "1990.02.17"},
    ]

    upcoming_birthdays = get_upcoming_birthdays(users)
    print("Список привітань на цьому тижні:", upcoming_birthdays)
