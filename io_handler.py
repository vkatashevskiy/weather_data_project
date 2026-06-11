# файл читает csv
import csv
import os

def read_csv(filename):
    if not os.path.exists(filename): # Проверяем существует ли файл
        raise FileNotFoundError(f"Файл '{filename}' не найден.")

    data = []

    with open(filename, mode='r', encoding='utf-8') as file:
        header = file.readline().strip().split(',') # Читаем первую строку (заголовки), чтобы проверить формат
        expected_header = ['year', 'month', 'day', 'temperature']

        if header != expected_header: # Проверяем корректен ли формат (заголовки)
            raise ValueError(f"Некорректный формат CSV. Ожидались заголовки: {expected_header}")

        file.seek(0) # Возвращаем указатель в начало файла и пропускаем заголовок для csv.Reader
        next(file)

        for line_number, line in enumerate(file, start=2): # Читаем остальные строки
            stripped_line = line.strip()

            if not stripped_line: # Проверяем отсутствуют ли пустые строки
                raise ValueError(f"Ошибка: обнаружена пустая строка на позиции {line_number}.")

            reader = csv.reader([stripped_line]) # Разбираем строку через csv.reader, чтобы правильно обработать разделители
            row = next(reader)

            if len(row) != 4: # Проверяем, что в строке ровно 4 элемента
                raise ValueError(f"Ошибка в строке {line_number}: неверное количество колонок.")

            try: # Преобразуем значения в числа
                row_dict = {
                    "year": int(row[0]),
                    "month": int(row[1]),
                    "day": int(row[2]),
                    "temperature": int(row[3])
                }
                data.append(row_dict)
            except ValueError:
                raise ValueError(f"Ошибка в строке {line_number}: данные должны быть числами.")

    return data


if __name__ == "__main__":
    name_of_file = "weather.csv"

    try:
        weather_data = read_csv(name_of_file)  # Вызываем функцию и сохраняем результат в переменную

        print("Данные успешно прочитаны:") # Красиво выводим результат в консоль

    except Exception as e:
        print(f"Произошла ошибка при чтении: {e}") # Если какая-то проверка не пройдется, мы увидим ошибку здесь
