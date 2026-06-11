class Node:
    """
    Класс узла стека: data - значение элемента, next - ссылка на следующий узел
    """
    def __init__(self, data):
        """
        Создает пустой узел
        """
        self.data = data
        self.next = None

class Stack:
    """
    Реализация стека на связном списке: top - вершина стека
    """
    def __init__(self):
        """
        Создает пустой стек
        """
        self.top = None
        self._size = 0

    def is_empty(self):
        """
        Проверяет стек на пустоту
        """
        return self.top is None

    def push(self, data):
        """
        Добавляет элемент в стек
        """
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        """
        Удаляет элемент из стека
        """
        if self.is_empty():
            return None
        value = self.top.data
        self.top = self.top.next
        self._size -= 1
        return value

    def peek(self):
        """
        Показывает верхушку стека
        """
        if self.is_empty():
            return None
        return self.top.data

    def size(self):
        """
        Выводит размер стека
        """
        return self._size
