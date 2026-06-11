import os
from io_handler import read_csv
from analyzer import (
    build_prefix_sums,
    average_by_month,
    find_max_temperature,
    find_min_temperature,
    sort_months
)
from bst import Tree
from queue import moving_average
from stack import Stack

def save_report(weather_data, is_smoothed, filename="weather_report.txt"):
    """
    Генерирует текстовый отчёт на основе текущих данных в программе и
    связывает результаты работы аналитика со статусом данных от пользователя.
    """
    # пересчитываем метрики по тому массиву, который сейчас активен
    prefix_sums = build_prefix_sums(weather_data)
    averages = average_by_month(weather_data, prefix_sums)
    max_date, max_temp = find_max_temperature(weather_data)
    min_date, min_temp = find_min_temperature(weather_data)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("ИТОГОВЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ О ПОГОДЕ \n")

        # интерактивный статус данных — показывает связь модулей
        status = "Да (7-дневное скользящее среднее)" if is_smoothed else "Нет (Исходные данные)"
        f.write(f"Ряд данных сглажен: {status}\n")
        f.write(f"Всего проанализировано дней: {len(weather_data)}\n\n")

        f.write("ТЕМПЕРАТУРНЫЕ РЕКОРДЫ ЗА ПЕРИОД\n")
        f.write(f"Самый теплый день: {max_date} ({max_temp}°C)\n")
        f.write(f"Самый холодный день: {min_date} ({min_temp}°C)\n\n")

        f.write("СРЕДНЯЯ ТЕМПЕРАТУРА ПО МЕСЯЦАМ\n")
        for month, temp in averages.items():
            f.write(f"Месяц {month:02d}: {temp}°C\n")

def print_menu():
    """
    Выводит текстовое консольное меню для пользователя
    """
    print("СИСТЕМА АНАЛИЗА ПОГОДНЫХ ДАННЫХ")
    print("1. Показать среднюю температуру по месяцам")
    print("2. Найти самый тёплый день за год")
    print("3. Найти самый холодный день за год")
    print("4. Отсортировать месяцы по температуре")
    print("5. Найти дни теплее заданной температуры (BST)")
    print("6. Выполнить сглаживание ряда (Очередь 7 дней)")
    print("7. Отменить последнее сглаживание (Стек)")
    print("8. Сохранить текущий аналитический отчёт в файл")
    print("0. Выход из программы")

def main():
    filename = "weather.csv"

    # первичная загрузка данных при старте программы
    try:
        # читаем данные из CSV. Теперь weather_data — наш основной рабочий список.
        weather_data = read_csv(filename)
        print(f"Успешно загружено дней: {len(weather_data)}")
    except Exception as e:
        print(f"Ошибка при старте программы: {e}")
        return

    # инициализируем стек для хранения истории (нужен для отмены сглаживания)
    history_stack = Stack()

    # флаг состояния данных (сглажены или исходные)
    is_smoothed = False

    while True:
        print_menu()
        choice = input("Выберите пункт меню (0-8): ").strip()

        if choice == "1":
            if not weather_data:
                print("Данные пусты.")
                continue
            prefix_sums = build_prefix_sums(weather_data)
            averages = average_by_month(weather_data, prefix_sums)

            print("\nСРЕДНЯЯ ТЕМПЕРАТУРА ПО МЕСЯЦАМ")
            for month, temp in averages.items():
                print(f"Месяц {month:02d}: {temp}°C")

        elif choice == "2":
            result = find_max_temperature(weather_data)
            if result:
                date_str, max_temp = result
                print(f"\nСамый тёплый день: {date_str} ({max_temp}°C)")
            else:
                print("Данные отсутствуют.")

        elif choice == "3":
            result = find_min_temperature(weather_data)
            if result:
                date_str, min_temp = result
                print(f"\nСамый холодный день: {date_str} ({min_temp}°C)")
            else:
                print("Данные отсутствуют.")

        elif choice == "4":
            if not weather_data:
                print("Данные пусты.")
                continue
            prefix_sums = build_prefix_sums(weather_data)
            averages = average_by_month(weather_data, prefix_sums)
            sorted_averages = sort_months(averages)

            print("\nМЕСЯЦЫ, ОТСОРТИРОВАННЫЕ ПО ВОЗРАСТАНИЮ ТЕМПЕРАТУРЫ")
            for month, temp in sorted_averages.items():
                print(f"Месяц {month:02d}: {temp}°C")

        elif choice == "5":
            if not weather_data:
                print("Данные отсутствуют.")
                continue

            # строим бинарное дерево поиска из текущего состояния данных
            root = Tree(weather_data[0])
            for record in weather_data[1:]:
                root.insert(record)

            try:
                threshold = float(input("Введите пороговую температуру: "))
                warmer_days = root.find_warmer_days(threshold)

                print(f"\nНайдено дней теплее {threshold}°C: {len(warmer_days)}")
                # выводим первые 15 результатов
                for record in warmer_days[:15]:
                    print(f"{record['day']:02d}.{record['month']:02d}.{record['year']}: {record['temperature']}°C")
                if len(warmer_days) > 15:
                    print(f"... и ещё {len(warmer_days) - 15} дн.")
            except ValueError:
                print("Ошибка: Введите корректное число.")

        elif choice == "6":
            # сохраняем старый массив в стек перед изменением
            history_stack.push(list(weather_data))

            # выполняем сглаживание и меняем флаг
            weather_data = moving_average(weather_data)
            is_smoothed = True
            print("\nСкользящее среднее успешно рассчитано.")

        elif choice == "7":
            if not history_stack.is_empty():
                # восстанавливаем данные и возвращаем флаг
                weather_data = history_stack.pop()
                is_smoothed = False
                print("\nПоследнее сглаживание успешно отменено. Данные восстановлены.")
            else:
                print("\nИстория изменений пуста. Отмена невозможна.")

        elif choice == "8":
            if not weather_data:
                print("Данные пусты. Нечего сохранять.")
                continue

            # выгружаем интерактивный отчет
            save_report(weather_data, is_smoothed)
            print("\nОтчёт успешно сохранен в файл 'weather_report.txt'")

        elif choice == "0":
            print("\nПрограмма завершена. До встречи!")
            break
        else:
            print("Ошибка ввода. Выберите пункт от 0 до 8.")

if __name__ == "__main__":
    main()
