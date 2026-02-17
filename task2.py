import random


def get_numbers_ticket(min_value: int, max_value: int, quantity: int) -> list[int]:
    """
    Генерує відсортований список унікальних випадкових чисел
    у діапазоні [min_value, max_value].
    Якщо параметри некоректні — повертає порожній список.
    """
    if (
        not isinstance(min_value, int)
        or not isinstance(max_value, int)
        or not isinstance(quantity, int)
    ):
        return []

    if min_value < 1 or max_value > 1000:
        return []

    if min_value > max_value:
        return []

    if quantity <= 0 or quantity > (max_value - min_value + 1):
        return []

    numbers = random.sample(range(min_value, max_value + 1), quantity)
    return sorted(numbers)


if __name__ == "__main__":
    lottery_numbers = get_numbers_ticket(1, 49, 6)
    print("Ваші лотерейні числа:", lottery_numbers)
