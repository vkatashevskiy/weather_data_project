# префиксные суммы, поиск максимума и минимума, сортировка
import numpy as np
def build_prefix_sums(weather_data):
    """
    Принимает список словарей с данными о погоде
    и возвращает массив префиксных сумм температур.
    """
    if not weather_data: # Если данных нет, возвращаем [0]
        return [0]

    prefix_sums = [0] # Первый элемент равен 0, для упрощения дальнейших расчетов

    current_sum = 0
    for record in weather_data:
        current_sum += record["temperature"] # Достаем температуру из словаря и прибавляем к текущей сумме
        prefix_sums.append(current_sum)

    return prefix_sums


def average_by_month(weather_data, prefix_sums):
    """
    Вычисляет среднюю температуру для каждого месяца,
    используя массив префиксных сумм.
    """
    if not weather_data or len(prefix_sums) != len(weather_data) + 1:
        return {}

    months_indices = {} # Группируем индексы дней по месяцам
    for index, record in enumerate(weather_data):
        month = record["month"]
        if month not in months_indices:
            months_indices[month] = []
        months_indices[month].append(index)

    monthly_averages = {}

    for month, indices in months_indices.items(): # Считаем среднее для каждого месяца через префиксные суммы
        start_idx = indices[0] # Индекс первого и последнего дня месяца в исходном списке
        end_idx = indices[-1]

        days_count = len(indices) # Количество дней в месяце

        month_sum = prefix_sums[end_idx + 1] - prefix_sums[start_idx] # Формула префиксных сумм

        monthly_averages[month] = round(month_sum / days_count, 2) # Считаем среднее и округляем до 2 знаков после запятой

    return monthly_averages


def find_max_temperature(weather_data):
    """
    Линейным поиском определяет самый тёплый день.
    Возвращает кортеж: (дата в формате ДД.ММ.ГГГГ, температура)
    """
    if not weather_data:
        return None  # Если данных нет, возвращаем ничего

    max_record = weather_data[0] # Инициализируем начальное максимальное значение первым элементом списка

    for record in weather_data[1:]: # Линейный поиск: перебираем все элементы со второго до последнего
        if record["temperature"] > max_record["temperature"]:
            max_record = record

    date_str = f"{max_record['day']:02d}.{max_record['month']:02d}.{max_record['year']}"
    max_temp = max_record["temperature"]

    return date_str, max_temp


def find_min_temperature(weather_data):
    """
    Линейным поиском определяет самый холодный день.
    Возвращает кортеж: (дата в формате ДД.ММ.ГГГГ, температура)
    """
    if not weather_data:
        return None  # Если данных нет, возвращаем ничего

    min_record = weather_data[0] # Инициализируем начальное минимальное значение первым элементом списка

    for record in weather_data[1:]: # Линейный поиск: перебираем все элементы со второго до последнего
        if record["temperature"] < min_record["temperature"]:
            min_record = record

    date_str = f"{min_record['day']:02d}.{min_record['month']:02d}.{min_record['year']}"
    min_temp = min_record["temperature"]

    return date_str, min_temp


def sort_months(monthly_averages):
    """
    Сортирует месяцы по средней температуре.
    Возвращает новый отсортированный словарь.
    """
    items = list(monthly_averages.items()) # Превращаем словарь в список кортежей вида [(месяц, температура), ... ]

    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        else:
            low = arr[0]
            high = arr[len(arr) - 1]
            demi = arr[len(arr) // 2]

            # Находим медиану по температурам (индекс 1)
            pivot = np.median([low[1], high[1], demi[1]])

            left = [i for i in arr if i[1] < pivot]
            equal = [k for k in arr if k[1] == pivot]
            right = [j for j in arr if j[1] > pivot]

        return quick_sort(left) + equal + quick_sort(right)

    sorted_list = quick_sort(items)
    # Превращаем отсортированный список кортежей обратно в словарь
    return dict(sorted_list)
