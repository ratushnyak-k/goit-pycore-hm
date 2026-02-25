def total_salary(path):
    """
    Аналізує текстовий файл із зарплатами розробників.
    Формат кожного рядка: Прізвище,зарплата
    Повертає кортеж (загальна сума, середня зарплата).
    """
    try:
        salaries = []

        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) < 2:
                    continue
                salary = float(parts[1].strip())
                salaries.append(salary)

        if not salaries:
            return (0, 0)

        total = sum(salaries)
        average = total / len(salaries)
        return (total, average)

    except FileNotFoundError:
        print(f"Помилка: файл '{path}' не знайдено.")
        return (0, 0)
    except ValueError as e:
        print(f"Помилка формату даних: {e}")
        return (0, 0)


if __name__ == "__main__":
    total, average = total_salary("salary.csv")
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
