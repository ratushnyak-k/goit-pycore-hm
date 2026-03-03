import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Повертає генератор, який ітерується по всіх дійсних числах у тексті.
    Вважаємо, що числа коректні та відокремлені пробілами.
    """

    pattern = r"\d+\.\d+|\d+"
    for match in re.finditer(pattern, text):
        yield float(match.group())



def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Використовує передану функцію-генератор для обчислення
    загальної суми всіх дійсних чисел у тексті.
    """
    return sum(func(text))


if __name__ == "__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."

    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # очікуємо 1351.46
