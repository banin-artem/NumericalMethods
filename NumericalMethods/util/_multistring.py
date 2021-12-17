class MultiString:
    """
    Класс строки, позволяющий складывать многострочные строки (мультистрока)
    """

    __string = ''

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __copy__(self):
        return self.copy()

    def __add__(self, other):
        if not isinstance(other, MultiString):
            try:
                return self + other.multistring
            except AttributeError:
                return self + MultiString(str(other))
        original = self.copy()
        other = other.copy()
        while original.rows_num < other.rows_num:
            original.append('')
        while other.rows_num < original.rows_num:
            other.append('')
        return MultiString([row_1 + row_2
                           for row_1, row_2 in zip(list(map(lambda x: x.ljust(self.max_row_len, ' '), self.rows)),
                                                   other.rows)])

    def add_r_separator(self, separator_border='|', separator_width=9, separator_fillchar=' '):
        """
        Добавление разделителя справа

        Args:
            separator_border (str): символ-разделитель
            separator_width (int): ширина разделителя
            separator_fillchar (str): заполнение строки-разделителя

        Returns:
            MultiString: строка с разделителем

        """
        separator_list = [separator_border.center(separator_width, separator_fillchar)
                          for row_no in range(self.rows_num)]
        return self + MultiString(separator_list)

    def add_l_separator(self, separator_border='|', separator_width=9, separator_fillchar=' '):
        """
        Добавление разделителя слева

        Args:
            separator_border (str): символ-разделитель
            separator_width (int): ширина разделителя
            separator_fillchar (str): заполнение строки-разделителя

        Returns:
            MultiString: строка с разделителем

        """
        separator_list = [separator_border.center(separator_width, separator_fillchar)
                          for row_no in range(self.rows_num)]
        return MultiString(separator_list) + self

    def add_with_separator(self, other, *args, **kwargs):
        """
        Сложение мультистрок с автоматическим выбором разделителя.

        Args:
            other: вторая мультистрока
            separator_border (str): символ-разделитель
            separator_width (int): ширина разделителя
            separator_fillchar (str): заполнение строки-разделителя

        Returns:
            MultiString: сумма строк с разделителем

        """
        if not isinstance(other, MultiString):
            try:
                other = other.multistring
            except AttributeError:
                other = MultiString(str(other))
        left = self.copy()
        right = other.copy()
        if left.rows_num > right.rows_num:
            left = self.add_r_separator(*args, **kwargs)
        else:
            right = right.add_l_separator(*args, **kwargs)
        return left + right

    def copy(self):
        """
        Возвращает копию мультистроки

        Returns:
            MultiString: копия мультистроки

        """
        return self

    def append(self, value):
        """
        Добавление новой строчки к мультистроке. Меняет исходную

        Args:
            value (Any): новая строчка

        Returns:
            None
        """
        value = str(value)
        self.string += '\n' + value

    @property
    def max_row_len(self):
        """
        Returns:
            int: максимальная длина строки в мультистроке

        """
        return max(map(len, self.rows))

    @property
    def rows(self):
        """
        Returns:
            list: список строк мультистроки

        """
        return self.string.split('\n')

    @property
    def rows_num(self):
        """
        Returns:
            int: количество строк в мультистроке

        """
        return len(self.rows)

    @property
    def string(self):
        """
        Returns:
            str: строка мультистроки
        """
        return self.__string

    @string.setter
    def string(self, new_value):
        if isinstance(new_value, str):
            self.__string = new_value
        elif isinstance(new_value, (list, tuple)):
            self.__string = '\n'.join(map(str, new_value))
        else:
            self.__string = str(new_value)
