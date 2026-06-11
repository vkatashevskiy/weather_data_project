import csv
import os

def read_csv(filename):
    if not os.path.exists(filename): # проверяем существует ли файл
        raise FileNotFoundError(f"Файл '{filename}' не найден.")

    data = []

    with open(filename, mode='r', encoding='utf-8') as file:
        header = file.readline().strip().split(',') # читаем первую строку (заголовки), чтобы проверить формат
        expected_header = ['year', 'month', 'day', 'temperature']

        if header != expected_header: # проверяем корректен ли формат (заголовки)
            raise ValueError(f"Некорректный формат CSV. Ожидались заголовки: {expected_header}")

        file.seek(0) # возвращаем указатель в начало файла и пропускаем заголовок для csv.Reader
        next(file)

        for line_number, line in enumerate(file, start=2): # читаем остальные строки
            stripped_line = line.strip()

            if not stripped_line: # проверяем отсутствуют ли пустые строки
                raise ValueError(f"Ошибка: обнаружена пустая строка на позиции {line_number}.")

            reader = csv.reader([stripped_line]) # разбираем строку через csv.reader, чтобы правильно обработать разделители
            row = next(reader)

            if len(row) != 4: # проверяем, что в строке ровно 4 элемента
                raise ValueError(f"Ошибка в строке {line_number}: неверное количество колонок.")

            try: # преобразуем значения в числа
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
