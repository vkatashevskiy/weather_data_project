class Node:
    """
    Класс узла очереди
    """
    def __init__(self, data):
        """
        Создает новый узел
        """
        self.data = data
        self.next = None

class Queue:
    """
    Очередь, реализованная через связный список: _front - первый добавленный элемент очереди, _rear - последний
    добавленный элемент очереди, _size - размер очереди
    """
    def __init__(self):
        """
        Создает пустую очередь
        """
        self._front = None
        self._rear = None
        self._size = 0

    def enqueue(self, data):
        """
        Добавляет элемент в очередь
        """
        self._size += 1
        node = Node(data)
        if self._rear is None:
            self._front = node
            self._rear = node
        else:
            self._rear.next = node
            self._rear = node

    def dequeue(self):
        """
        Удаляет элемент из очереди
        """
        if self._front is None:
            raise IndexError('empty queue')
        value = self._front.data
        self._front = self._front.next
        # если после удаления _front оказался пустым, то и _rear становится пустым
        if self._front is None:
            self._rear = None
        self._size -= 1
        return value

    def size(self):
        """
        Выводит размер очереди
        """
        return self._size

    def is_empty(self):
        """
        Проверяет очередь на пустоту
        """
        return self._front is None

    def sum_values(self):
        """
        Суммирует значения температуры
        """
        current = self._front
        total = 0
        while current:
            total += current.data
            current = current.next
        return total

def moving_average(weather_data):
    """
    Считает скользящее среднее с окном 7 дней
    """
    smoothed = []
    queue = Queue()

    for record in weather_data:
        temp = record['temperature']
        queue.enqueue(temp)

        # если в очереди накопилось больше 7 дней, то удаляем самый старый
        if queue.size() > 7:
            queue.dequeue()

        # среднее по текущему окну
        current_window_sum = queue.sum_values()
        current_window_size = queue.size()
        smoothed_temp = round(current_window_sum/current_window_size, 2)

        # копия словаря
        smoothed_record = {
            'year': record['year'],
            'month': record['month'],
            'day': record['day'],
            'temperature': smoothed_temp
        }
        smoothed.append(smoothed_record)

    return smoothed
