class Tree:
    """
    Класс узла бинарного дерева поиска для хранения температур и списков дней
    """
    def __init__(self, record):
        """
        Инициализирует новый узел дерева на основе словаря
        """
        self.key = record['temperature']
        self.records = [record]
        self.left_child = None
        self.right_child = None

    def insert(self, record):
        """
        Вставляет элемент бинарного дерева поиска на нужное место и если температура совпадает, то добавляется запись
        в список текущего узла
        """
        value = record['temperature']

        # если температура совпала
        if value == self.key:
            self.records.append(record)

        # элемент меньше корня, тогда уходим в левое поддерево
        elif value < self.key:
            # нет левого ребенка, создаем узел
            if self.left_child is None:
                self.left_child = Tree(record)
            # рекурсивно вызываем insert
            else:
                self.left_child.insert(record)

        # элемент больше корня, тогда уходим в правое поддерево
        elif value > self.key:
            # нет правого ребенка, создаем узел
            if self.right_child is None:
                self.right_child = Tree(record)
            # рекурсивно вызываем insert
            else:
                self.right_child.insert(record)

    def preorder(self):
        """
        Осуществляет прямой обход дерева: корень - левое поддерево - правое поддерево
        """
        print(f'[{self.key}°C: {len(self.records)} дн.]', end=' ')
        if self.left_child is not None:
            self.left_child.preorder()

        if self.right_child is not None:
            self.right_child.preorder()

    def _find_warmer_recursive(self, current, threshold_temp, res):
        """
        Метод рекурсивного обхода для сбора теплых дней
        """
        # базовый случай: если дошли до пустого узла
        if current is None:
            return

        # температура в узле выше пороговой
        if current.key > threshold_temp:
            res.extend(current.records) # узел подходит, берем все накопившиеся дни
            self._find_warmer_recursive(current.right_child, threshold_temp, res) # в правом значения больше, идем туда
            self._find_warmer_recursive(current.left_child, threshold_temp, res) # в левом меньше корня, но могут быть значения выше порога

        else:
            # если текущий узел меньше или равен порогу, то все левое поддерево точно меньше порога
            # отсекаем левую ветку и ищем только в правой
            self._find_warmer_recursive(current.right_child, threshold_temp, res)

    def find_warmer_days(self, threshold_temp):
        """
        Находит все дни, где температура выше заданной
        """
        res = []
        self._find_warmer_recursive(self, threshold_temp, res) # рекурсивный обход дерева, текущий корень дерева
        # передается как стартовая точка
        return res
