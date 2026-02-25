def get_cats_info(path):
    """
    Читає текстовий файл із даними про котів.
    Формат кожного рядка: id,ім'я,вік
    Повертає список словників з ключами 'id', 'name', 'age'.
    """
    cats = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) < 3:
                    continue
                cat = {
                    "id": parts[0].strip(),
                    "name": parts[1].strip(),
                    "age": parts[2].strip(),
                }
                cats.append(cat)

    except FileNotFoundError:
        print(f"Помилка: файл '{path}' не знайдено.")
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")

    return cats


if __name__ == "__main__":
    cats_info = get_cats_info("cats.csv")
    print(cats_info)
