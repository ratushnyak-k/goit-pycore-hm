from datetime import datetime


def get_days_from_today(date: str) -> int:
    """
    Повертає кількість днів між заданою датою (YYYY-MM-DD)
    та поточною датою. Якщо дата в майбутньому - число від'ємне.
    """
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Дата повинна бути у форматі 'YYYY-MM-DD'")

    today = datetime.today().date()
    delta = today - target_date
    return delta.days


if __name__ == "__main__":
    print(get_days_from_today("2020-10-09"))
    print(get_days_from_today("2026-10-09"))
