import pickle
import random as rnd

from NumericalMethods.util.sympy_init import *
from NumericalMethods.util import MultiString
import NumericalMethods._determinant as determinant
from NumericalMethods.first_problem_direct import kramer, triple


def det(*args, **kwargs) -> (int, float):
    """Автоматическое нахождение определителя"""
    return determinant.auto_det(*args, **kwargs)


class Matrix:
    """Класс, содержащий методы работы с матрицами и векторами (матрицами с одним столбцом или строкой)"""

    __matrix = []

    def __init__(self, *args, **kwargs):
        if len(args) == 1:  # случай, когда при инициализации передан один аргумент
            if isinstance(args[0], int):  # если этот агрумент - число, создается квадратная матрица
                self.matrix = [[0 for j in range(args[0])] for i in range(args[0])]
            elif isinstance(args[0], list):  # если этот аргумент - список, проверяестя наличие в нем списков
                if isinstance(args[0][0], list):  # если двумерный - оставить как есть, иначе - считать его строкой
                    self.matrix = args[0]         # матрицы (полезно для векторов)
                else:
                    self.matrix = [args[0]]
            elif isinstance(args[0][0], Matrix):
                self.matrix = args[0][0].copy().matrix  # на случай если этот аргумент - матрица
            else:
                raise TypeError("Неизвестный тип данных, используйте list, или int, или int, int")
        elif len(args) == 2:
            if isinstance(args[0], int) and isinstance(args[1], int):  # если аргументов два - создается прямоугольная
                self.matrix = [[0 for j in range(args[1])] for i in range(args[0])]  # прямоугольная матрица
        else:
            raise ValueError("Слишком много аргументов")

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        if len(value) != self.columns:
            raise IndexError("Ширина новой строки не совпадает с шириной матрицы")
        self.matrix[key] = value

    def __str__(self):
        out = f'Матрица {self.size}\n'
        for row in self.matrix:
            out += str(row) + '\n'
        return out

    def __add__(self, other):
        if isinstance(other, (float, int)):  # сложение матрицы с числом
            matrix = self.copy()
            for row_no, col_no in self:
                matrix[row_no][col_no] += other
            return matrix
        elif isinstance(other, Matrix):  # сложение матрицы с матрицей
            if self.size != other.size:
                raise ArithmeticError("Нельзя сложить матрицы разного размера")
            matrix = self.copy()
            for row_no, col_no in self:
                matrix[row_no][col_no] += other[row_no][col_no]
            return matrix

    def __mul__(self, other):
        if isinstance(other, Matrix):  # умножение матрицы на число или на вектор
            if self.columns != other.rows:
                if not self.is_vector and not other.is_vector:
                    raise IndexError("Количество столбцов первой матрицы не совпадает с количеством строк второй")
                else:
                    try:
                        return self * other.T
                    except IndexError:
                        return self.T * other
            matrix = Matrix(self.rows, other.columns)
            for i in self.r_rows:
                for j in other.r_cols:
                    for s in self.r_cols:
                        if self.rows > 1:
                            matrix[i][j] += self[i][s] * other[s][j]
                        else:
                            matrix[i][j] += self[s] * other[s][j]
            return matrix
        else:
            matrix = self.copy()  # умножение матрицы на число
            for row_no, col_no in self:
                matrix[row_no][col_no] *= other
            return matrix

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        return self * other ** (-1)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.matrix == other.matrix  # при сравнении матриц сравниваются их списки
        else:
            return False

    def __hash__(self):
        return hash(tuple(map(tuple, self.matrix)))

    def __len__(self):
        return self.columns * self.rows

    def __iter__(self):
        def iterator():
            for row_no in self.r_rows:
                for col_no in self.r_cols:
                    yield row_no, col_no
        return iterator()

    def __pow__(self, power, modulo=None):
        new_matrix = self.copy()
        if power == 0:
            new_matrix.fill_diagonal_ones()  # любая матрица в степени 0 - единичная матрица
            return new_matrix
        elif power == 1:
            return new_matrix
        elif power == -1:
            if det(new_matrix) == 0:
                raise ArithmeticError("Невозможно найти обратную матрицу так как определитель равен нулю")
            else:
                return new_matrix.complements.T / det(new_matrix)  # нахождение обратной матрицы
        elif power > 1:
            return new_matrix * new_matrix ** (power - 1)  # поиск степени матрицы через рекурсию
        else:
            new_matrix = new_matrix ** (-1)
            return new_matrix ** (-power)

    def map(self, func: callable, *args, **kwargs):
        """
        Применяет указанную функцию ко всем элементам матрицы с указанными далее аргументами

        Examples:
            >>>matrix = Matrix(3)
            >>>matrix.map(abs)

        Args:
            func (callable): Функция, которая будет применена к каждому элементу матрицы
            *args (): Аргументы, с которыми будет применена функция
            **kwargs (): Ключевые аргументы, с которыми будет применена функция

        Returns:
            Matrix: новая матрица

        """
        matrix = self.copy()
        for row_no, col_no in matrix:
            matrix[row_no][col_no] = func(matrix[row_no][col_no], *args, **kwargs)
        return matrix

    def console_display(self) -> None:
        """
        Красиво печатет матрицу в консоль
        """
        print(f'Матрица {self.size}'.center(self.columns * (self.max_len_num + 3) - 1))
        print(self.to_pretty_string())

    def fill_random(self, start: (int, float) = -10, stop: (int, float) = 10) -> None:
        """
        Заполняет матрицу случайными числами, принадлежащими указанному отрезку. Меняет исходную матрицу.
        Если указанные края отрезка - целые числа, матрица будет заполнена целыми числами,
        иначе - числами с плавающей точкой

        Args:
            start (int, float): левый край отрезка (по умолчанию -10)
            stop (int, float): правый край отрезка (по умолчанию 10)

        Returns:
            None

        Raises:
              IndexError: если длина выбранного отрезка равна нулю

        """
        start, stop = min(start, stop), max(start, stop)
        if stop - start == 0:
            raise IndexError("Выбран пустой диапазон")
        if isinstance(start, float) or isinstance(stop, float):
            self.matrix = [[rnd.uniform(start, stop) for col_no in self.r_cols] for row_no in self.r_rows]
        else:
            self.matrix = [[rnd.randint(start, stop) for col_no in self.r_cols] for row_no in self.r_rows]

    def fill_value(self, value=1) -> None:
        """
        Заполняет матрицу указанным значением. Меняет исходную матрицу.

        Args:
            value (Any): значение-наполнитель (по умолчанию 1)

        Returns:
            None
        """
        self.matrix = [[value for col_no in self.r_cols] for row_no in self.r_rows]

    def fill_diagonal_ones(self) -> None:
        """
        Превращает матрицу в единичную. Меняет исходную матрицу.

        Returns:
            None

        Raises:
              TypeError: если матрица не является квадратной

        """
        if not self.is_square:
            raise TypeError("Невозможно составить единичную матрицу из не квадратной матрицы")
        self.matrix = [[1 if row_no == col_no else 0 for col_no in self.r_cols] for row_no in self.r_rows]

    def fill_sequence(self, start: int = 1) -> None:
        """
        Заполняет матрицу последовательно увеличивающимися числами. Меняет исходную матрицу.
        Например:

        1 2 3

        4 5 6

        7 8 9

        Args:
            start (int): начальное значение (по умолчанию 1)

        Returns:
            None
        """
        self.matrix = [[start + col_no + row_no * self.columns for col_no in self.r_cols] for row_no in self.r_rows]

    def fill_H_grid(self, fill_value_1=0, fill_value_2=1, step: int = 1) -> None:
        """
        Заполняет матрицу сеткой значений. Меняет исходную матрицу.
        Например:

        1 0 1 0 1

        1 1 1 1 1

        1 0 1 0 1

        1 1 1 1 1

        Args:
            fill_value_1 (Any): первое значение-наполнитель (по умолчанию 0)
            fill_value_2 (Any): второе значение-наполнитель (по умолчанию 1)
            step (int): шаг сетки (по умолчанию 1)

        Returns:
            None
        """
        self.matrix = [[fill_value_1 if bool(row_no % (step + 1)) or bool(col_no % (step + 1)) else fill_value_2
                        for col_no in self.r_cols]
                       for row_no in self.r_rows]

    def fill_X_grid(self, fill_value_1=0, fill_value_2=1, step: int = 1) -> None:
        """
        Заполняет матрицу сеткой значений. Меняет исходную матрицу.
        Например:

        1 0 1 0 1

        0 1 0 1 0

        1 0 1 0 1

        0 1 0 1 0

        1 0 1 0 1

        Args:
            fill_value_1 (Any): первое значение-наполнитель (по умолчанию 0)
            fill_value_2 (Any): второе значение-наполнитель (по умолчанию 1)
            step (int): шаг сетки (по умолчанию 1)

        Returns:
            None
        """
        self.matrix = [[fill_value_1 if row_no % (step + 1) == col_no % (step + 1) else fill_value_2
                        for col_no in self.r_cols]
                       for row_no in self.r_rows]

    def fill_dominant(self, start: (int, float) = -10, stop: (int, float) = 10) -> None:
        """
        Заполняет матрицу случайными числами с преобладающей диагональю. Значения на главной диагонали могут выходить
        за пределы указанного отрезка. Меняет исходную матрицу.
        Если указанные края отрезка - целые числа, матрица будет заполнена целыми числами,
        иначе - числами с плавающей точкой

        Args:
            start (int, float): левый край отрезка (по умолчанию -10)
            stop (int, float): правый край отрезка (по умолчанию 10)

        Returns:
            None

        Raises:
              TypeError: если матрица не является квадратной

        """
        if not self.is_square:
            raise TypeError("Доминантной можно сделать только квадратную матрицу")
        new_matrix = Matrix(self.size[0], self.size[1])
        new_matrix.fill_random(start, stop)
        if isinstance(start, float) or isinstance(stop, float):
            random = rnd.uniform
        else:
            random = rnd.randint
        for row_no, col_no in new_matrix:
            if row_no == col_no:
                container = 0
                for col_no_inner in new_matrix.r_cols:
                    if col_no_inner != col_no:
                        container += abs(new_matrix[row_no][col_no_inner])
                # Гарантия доминации диагонали - значения в диагонали по модулю больше суммы модулей соостветствующих
                # соостветствующих строк на случайную величину
                new_matrix[row_no][col_no] = container + abs(random(start, stop))
                # Добавление отрицательных значений
                new_matrix[row_no][col_no] *= 1 if rnd.random() < 1 / self.rows else -1
        self.matrix = new_matrix.copy().matrix

    def fill_triple_diagonal(self, start: (int, float) = -10, stop: (int, float) = 10) -> None:
        """
        Заполняет три диагонали матрицы случайными числами из указанного отрезка. Меняет исходную матрицу.
        Если указанные края отрезка - целые числа, матрица будет заполнена целыми числами,
        иначе - числами с плавающей точкой

        Args:
            start (int, float): левый край отрезка (по умолчанию -10)
            stop (int, float): правый край отрезка (по умолчанию 10)

        Returns:
            None

        Raises:
              IndexError: если длина выбранного отрезка равна нулю
              TypeError: если матрица не является квадратной

        """
        if not self.is_square:
            raise TypeError("Трехдиагональной можно сделать только квадратную матрицу")
        start, stop = min(start, stop), max(start, stop)
        if stop - start == 0:
            raise IndexError("Выбран пустой диапазон")
        if isinstance(start, float) or isinstance(stop, float):
            random = rnd.uniform
        else:
            random = rnd.randint
        self.matrix = [[random(start, stop) if col_no == row_no or col_no - 1 == row_no or col_no == row_no - 1 else 0
                        for col_no in self.r_cols]
                       for row_no in self.r_rows]

    def fill_symbols(self, liter: str = 'a',
                     prefix: str = '',
                     postfix: str = '',
                     row_start: int = 0,
                     col_start: int = 0) -> None:
        """
        Заполняет матрицу символами Sympy. Меняет исходную матрицу.

        Args:
            liter (str): буква, обозначающая значение элемента матрицы (по умолчанию 'a')
            prefix (str): префикс (по умолчанию '')
            postfix (str): постфикс (по умолчанию '')
            row_start (int): начало нумерации строк (по умолчанию 0)
            col_start (int): начало нумерации столбцов. (по умолчанию 0)

        Returns:
            None
        """

        def getchar(row_no, col_no):
            return f'{prefix}{liter}{row_no + row_start}{col_no + col_start}{postfix}'

        self.matrix = [[Symbol(getchar(row_no, col_no)) for col_no in self.r_cols] for row_no in self.r_rows]

    def minor(self, row: int, column: int):
        """
        Удаляет из матрицы указанную строку и столбец
        (минор элемента это определитель результата работы этого метода)

        Examples:
            >>>matrix = Matrix(3)
            >>>matrix.minor(1, 1) # вернет матрицу без первой строки и столбца

        Args:
            row (int): номер строки
            column (int): номер столбца

        Returns:
            Matrix: новая матрица
        """
        matrix = self.copy()
        matrix.pop_row(row)
        matrix.pop_column(column)
        return matrix

    def add_column(self, col_no: int, n: (int, float)):
        """
        Сложение указанного столбца с указанным числом

        Examples:
            >>>matrix = Matrix(3)
            >>>matrix.add_column(1, .5) # прибавит к каждому элементу столбца 0.5

        Args:
            col_no (int): номер столбца
            n (int, float): число

        Returns:
            Matrix: новая матрица

        """
        matrix = self.copy()
        for row_no in self.r_rows:
            matrix.matrix[row_no][col_no] += n
        return matrix

    def add_row(self, row_no: int, n: (int, float)):
        """
        Сложение указанной строки с указанным числом

        Examples:
            >>>matrix = Matrix(3)
            >>>matrix.add_row(1, .7) # прибавит к каждому элементу первой строки 0.7

        Args:
            row_no (int): номер строки
            n (int, float): число

        Returns:
            Matrix: новая матрица

        """
        matrix = self.copy()
        matrix.matrix[row_no] = [elem + n for elem in matrix.matrix[row_no]]
        return matrix

    def mul_column(self, col_no: int, n: (int, float)):
        """
        Умножение указанного столбца на указанное число

        Examples:
            >>>matrix = Matrix(3)
            >>>matrix.mul_column(2, 0) # умножит второй столбец на 0

        Args:
            col_no (int): номер столбца
            n (int, float): число

        Returns:
            Matrix: новая матрица

        """
        matrix = self.copy()
        for row_no in self.r_rows:
            matrix.matrix[row_no][col_no] *= n
        return matrix

    def mul_row(self, row_no: int, n: (int, float)):
        """
        Умножение указанной строки на указанное число

        Examples:
            >>>matrix = Matrix(3)
            >>>matrix.mul_row(0, 0) # Умножит нулевую строку на 0

        Args:
            row_no (int): номер строки
            n (int, float): число

        Returns:
            Matrix: новая матрица

        """
        matrix = self.copy()
        matrix.matrix[row_no] = [elem * n for elem in matrix.matrix[row_no]]
        return matrix

    def pow_row(self, row_no: int, n: (int, float)):
        """
        Возведение указанной строки в указанную степень

        Examples:
            >>>matrix = Matrix(3)
            >>>matrix.pow_row(1, 2) # возведет в квадрат каждый элемент первой строки

        Args:
            row_no (int): номер строки
            n (int, float): степень

        Returns:
            Matrix: новая матрица

        """
        matrix = self.copy()
        matrix.matrix[row_no] = [elem ** n for elem in matrix.matrix[row_no]]
        return matrix

    def pow_column(self, col_no: int, n: (int, float)):
        """
        Возведение указанного столбца в указанную степень

        Args:
            col_no (int): номер столбца
            n (int, float): степень

        Returns:
            Matrix: новая матрица

        """
        new_matrix = self.copy()
        for row_no in new_matrix.r_rows:
            new_matrix[row_no][col_no] **= n
        return new_matrix

    def apply_mask(self, other):
        """
        Применяет маску (перемножает соответствующие элементы двух матриц)

        Args:
            other (Matrix): матрица-маска

        Returns:
            Matrix: новая матрица

        Raises:
            TypeError: если маска не является матрицей
            ArithmeticError: если маска не соответствеует размеру матрицы

        """
        if not isinstance(other, Matrix):
            raise TypeError("Маска тоже должна быть матрицей")
        if self.size != other.size:
            raise IndexError("Маска должна быть соответствующего размера")
        matrix = self.copy()
        for row_no, col_no in self:
            matrix.matrix[row_no][col_no] *= other.matrix[row_no][col_no]
        return matrix

    def swap_rows(self, row_1: int, row_2: int):
        """
        Меняет две строки местами

        Args:
            row_1 (int): номер первой строки
            row_2 (int): номер второй строки

        Returns:
            Matrix: новая матрица

        """
        new_matrix = self.copy()
        new_matrix[row_1], new_matrix[row_2] = new_matrix[row_2], new_matrix[row_1]
        return new_matrix

    def swap_columns(self, column_1: int, column_2: int):
        """
        Меняет два столбца местами

        Args:
            column_1 (int): номер первого столбца
            column_2 (int): номер второго столбика

        Returns:
            Matrix: новая матрица

        """
        matrix = self.copy()
        for row_no in range(self.rows):
            matrix[row_no][column_1], matrix[row_no][column_2] = matrix[row_no][column_2], matrix[row_no][column_1]
        return matrix

    def search_for_max_num_count(self, num=0) -> int:
        """
        Устарел
        Ищет строку с наибольшим количеством указаной величины (по умолчанию 0), если такой нет - вернет 0

        Args:
            num (Any): число, количество вхождений которого нужно определить

        Returns:
            int: номер строки с наибольшим количеством вхождений указаной величины, если такой нет - вернет 0

        """
        counter = self.matrix.count(num)
        max_nums_row_no = 0
        for row_no in self.r_rows:
            if self[row_no].count(num) > counter:
                counter = self[row_no].count(num)
                max_nums_row_no = row_no
        return max_nums_row_no

    def count_in_row(self, row_no: int, value, invert: bool = False) -> int:
        """
        Считает сколько содержится в указанной строке указанных элементов

        Args:
            row_no (int): номер строки
            value (Any): значение, количество вхождений которонго нужно определить
            invert (bool): флаг, если True, то ищет сколько элементов в строке не соответствует value

        Returns:
            int: количество вхождений элемента в строке

        """
        if not invert:
            return self.matrix[row_no].count(value)
        else:
            return self.columns - self.count_in_row(row_no, value)

    def count_in_column(self, col_no: int, value, invert: bool = False) -> int:
        """
        Считает сколько содержится в указанном столбце указанных элементов

        Args:
            col_no (int): номер столбца
            value (Any): значение, количество вхождений которонго нужно определить
            invert (bool): флаг, если True, то ищет сколько элементов в строке не соответствует value

        Returns:
            int: количество вхождений элемента в строке

        """
        if not invert:
            return self.T.matrix[col_no].count(value)
        else:
            return self.T.columns - self.count_in_column(col_no, value)

    def append_row(self, new_row: list) -> None:
        """
        Добавляет новую строку в матрицу. Меняет исходную матрицу
        Args:
            new_row (list): новая строка

        Returns:
            None

        Raises:
            IndexError: если длина новой строки не равна количеству столбцов матрицы

        """
        if len(new_row) == self.columns:
            self.matrix.append(new_row)
        else:
            raise IndexError("Ширина новой строки не равна ширине матрицы")

    def append_column(self, new_column: list) -> None:
        """
        Добавляет новый столбец в матрицу. Меняет исходную матрицу

        Args:
            new_column (list): новый столбец

        Returns:
            None

        Raises:
            IndexError: если количество элементов нового столбца не равна количеству строк матрицы

        """
        if len(new_column) != self.rows:
            raise IndexError("Высота нового столбца не равна высоте матрицы")
        else:
            for row, new_val in zip(self.matrix, new_column):
                row.append(new_val)

    def pop_column(self, col_no: int) -> list:
        """
        Удаляет столбец из матрицы. Меняет исходную матрицу

        Args:
            col_no (int): номер столбца

        Returns:
            list: удаленный столбец

        """
        out_col = []
        for row_no in self.r_rows:
            out_col.append(self.matrix[row_no].pop(col_no))
        return out_col

    def pop_row(self, row_no: int) -> list:
        """
        Удаляет строку из матрицы. Меняет исходную матрицу

        Args:
            row_no (int): номер строки

        Returns:
            list: удаленная строка
        """
        return self.matrix.pop(row_no)

    def insert_row(self, row_no: int, row: list) -> None:
        """
        Вставляет строку в указанное место в исходную матрицу. Меняет исходную матрицу

        Args:
            row_no (int): номер позиции
            row (list): новая строка

        Returns:
            None

        Raises:
            IndexError: если длина новой строки не равна количеству столбцов матрицы

        """
        if len(row) != self.columns:
            raise IndexError("Ширина новой строки не равна ширине матрицы")
        self.matrix.insert(row_no, row)

    def insert_column(self, col_no: int, col: list) -> None:
        """
        Вставляет столбец в указанное место в исходную матрицу. Меняет исходную матрицу

        Args:
            col_no (int): номер столбца
            col (list): новый столбец

        Returns:
            None

        Raises:
            IndexError: если количество элементов нового столбца не равна количеству строк матрицы

        """
        if len(col) != self.rows:
            raise IndexError("Высота нового столбца не равна высоте матрицы")
        for row_no in self.r_rows:
            self.matrix[row_no].insert(col_no, col[row_no])

    def dump_to_file(self, filename: str) -> None:
        """
        Записывает матрицу в файл

        Args:
            filename (str): имя файла

        Returns:
            None

        """
        with open(filename + '.matrix', 'wb') as file:
            pickle.dump(self.matrix, file)

    def to_pretty_string(self, round_to: int = 8) -> str:
        """
        Возвращает строку, содержащую матрицу сформированную таблицей

        Args:
            round_to (int): количество знаков после точки

        Returns:
            str: строковое представление таблицы

        """
        max_len_num = self.max_len_num
        pretty_string = ' ' + '_' * (self.columns * (max_len_num + 3) - 1) + ' \n'
        string_format = f':^{max_len_num + 2}.{round_to}f'
        string_format = '{' + string_format + '}'
        for row_no in self.r_rows:
            for col_no in self.r_cols:
                elem = self[row_no][col_no]
                if isinstance(elem, float):
                    pretty_string += '|' + string_format.format(elem)
                else:
                    pretty_string += f'|{str(elem).center(max_len_num + 2)}'
            pretty_string += "|\n" + ("|" + "_" * (max_len_num + 2)) * self.columns + "|\n"
        return pretty_string

    def copy(self):
        """
        Глубокая копия матрицы

        Returns:
            Matrix: новая матрица

        """
        return Matrix(list(map(list, self.matrix)))  # модуль copy и функция deepcopy сильно замедляли работу

    def _create_zero_column(self, column_no: int = 0, row_limit: int = 0):

        def mul_row(row, num):
            return [elem * num for elem in row]

        def sub_rows(no_to, row):
            self[no_to] = [elem1 - elem2 for elem1, elem2 in zip(self[no_to], row)]

        for row_no in range(self.rows - 1, row_limit, -1):
            try:
                new_row = mul_row(self[row_no - 1], self[row_no][column_no] / self[row_no - 1][column_no])
                sub_rows(row_no, new_row)
            except ZeroDivisionError:
                continue

    def triangulate(self):
        """
        Триангулирует матрицу

        Returns:
            Matrix: новая матрица

        """

        triangulated_matrix = self.copy()
        for col_no in self.r_cols:
            triangulated_matrix._create_zero_column(col_no, col_no)
        return triangulated_matrix

    def triangulate_to_ones(self):
        """
        Возвращает триангулированную матрицу с единицами в главной диагонали (возможно и нулями)

        Returns:
            Matrix: новая матрица

        """

        def mul_row(row, n):
            return [val * n for val in row]

        matrix = self.copy()
        matrix = matrix.triangulate()
        for row_no, col_no in matrix:
            if row_no == col_no:
                try:
                    matrix.matrix[row_no] = mul_row(matrix[row_no], 1 / matrix[row_no][col_no])
                except ZeroDivisionError:  # на случай, если в процессе триангуляции в главной диагонали окажется ноль
                    continue
        return matrix

    def vector_scalar_mul(self, other) -> (int, float):
        """
        Скалярное произведение векторов

        Args:
            other (Matrix): второй вектор (матрица с 1 столбцом или 1 строкой)

        Returns:
            int, float: результат скалярного произведения

        Raises:
            TypeError: если self или other не являются вектором (матрицей с 1 столбцом или 1 строкой)
            IndexError: если размерности векторов не равны

        """
        if not self.is_vector:
            TypeError("Скалярное произведение только для векторов (матриц с 1 столбцом или 1 строкой)")
        if isinstance(other, Matrix):
            if not other.is_vector:
                TypeError("Скалярное произведение только для векторов (матриц с 1 столбцом или 1 строкой)")
        else:
            return self.vector_scalar_mul(Matrix(other))
        if self.rows != other.rows and self.rows != other.T.rows:
            raise IndexError("Скалярное произведение можно найти только у векторов равной размерности")
        return sum((elem_1 * elem_2 for elem_1, elem_2 in zip(self.vector_to_list, other.vector_to_list)))

    def slau_solve(self, free_column: list) -> list:
        """
        Решение СЛАУ

        Args:
            free_column (list): столбец свободных членов

        Returns:
            list: список решений

        """
        return solve(self, free_column)

    @property
    def det(self) -> (int, float):
        """
        Returns:
            float: определитель матрицы

        """
        return det(self)

    @property
    def triangulated(self):
        """
        Returns:
            Matrix: триангулировання матрица

        """
        return self.triangulate()

    @property
    def matrix(self):
        """
        Returns:
            list: двумерный список, олицетворяющий матрицу

        """
        return self.__matrix

    @matrix.setter
    def matrix(self, new_value):
        if not isinstance(new_value, list):
            new_value = list(new_value)
        if len(new_value) == 0:
            new_value.append([])
        # проверка корректности новой матрицы
        for row_no in range(len(new_value)):
            if len(new_value[0]) != len(new_value[row_no]):
                raise IndexError("Длины строк матрицы не равны")
        self.__matrix = new_value

    @property
    def vector_to_list(self):
        """
        Преобразование вектора в список (только для матриц с одним столбцом или строкой)
        Returns:
            list: одномерный список, олицетворяющий вектор

        """
        if self.rows > 1:
            temp = self.T
            if temp.rows != 1:
                raise ArithmeticError("В список можно превратить только вектор")
            return temp.matrix[0]
        else:
            if self.rows != 1:
                raise ArithmeticError("В список можно превратить только вектор")
            return self.matrix[0]

    @property
    def vector_norma_1(self) -> (float, int):
        """
        Первая норма вектора (только для матриц с одним столбцом или строкой)

        Returns:
            float: первая норма вектора

        """
        return max(map(abs, self.vector_to_list))

    @property
    def vector_norma_2(self) -> (int, float):
        """
        Вторая норма вектора (только для матриц с одним столбцом или строкой)

        Returns:
            float: вторая норма вектора

        """
        return sum(map(abs, self.vector_to_list))

    @property
    def vector_norma_3(self) -> float:
        """
        Третья норма вектора (только для матриц с одним столбцом или строкой)

        Returns:
            float: третья норма вектора

        """
        return sum((element ** 2 for element in self.vector_to_list)) ** .5

    @property
    def norma_1(self) -> float:
        """
        Первая норма матрицы (по строкам)

        Returns:
            float: первая норма матрицы

        """
        return max((sum(map(lambda value: abs(value), row)) for row in self.matrix))

    @property
    def norma_2(self) -> float:
        """
        Вторая норма матрицы (по столбцам)

        Returns:
            float: вторая норма матрицы

        """
        norma = []
        for col_no in self.r_cols:
            col_value = 0
            for row_no in self.r_rows:
                col_value += abs(self[row_no][col_no])
            norma.append(col_value)
        norma = max(norma)
        return norma

    @property
    def norma_3(self) -> float:
        """
        Третья норма матрицы

        Returns:
            float: третья норма матрицы

        """
        return sum((self[row_no][col_no] ** 2 for row_no, col_no in self)) ** .5

    @property
    def is_dominant(self) -> bool:
        """
        Определяет является ли диагональ матрицы доминантной

        Returns:
            bool: является ли диагональ матрицы доминантной

        """
        if not self.is_square:
            return False
        for row_no in self.r_rows:
            summat = 0
            for col_no in self.r_cols:
                if row_no == col_no:
                    continue
                summat += abs(self[row_no][col_no])
            if summat > abs(self[row_no][row_no]):
                return False
        else:
            return True

    @property
    def max_len_num(self, round_to: int = 8):
        """
        Длина максимального строкового представления элемента матрицы. Для to_pretty_string

        Returns:
            int: длина максимального строкового представления элемента матрицы
        """
        container = 0
        format_string = '{' + f':.{round_to}f' + '}'
        for row in self.matrix:
            for element in row:
                if isinstance(element, float):
                    container = max(len(format_string.format(element)), container)
                else:
                    container = max(len(str(element)), container)
        return container

    @property
    def complements(self):
        """
        Матрица алгебраических дополнений

        Returns:
            Matrix: матрица алгебраических дополнений

        """
        matrix = self.copy()
        for row_no, col_no in self:
            matrix[row_no][col_no] = det(self.minor(row_no, col_no))
        for row_no, col_no in self:
            if bool((row_no + col_no) % 2):
                matrix[row_no][col_no] = -matrix[row_no][col_no]
        return matrix

    @property
    def T(self):
        """
        Транспонированная матрица

        Returns:
            Matrix: транспонированная матрица

        """
        return Matrix([list(new_column) for new_column in zip(*self.matrix)])

    @property
    def size(self) -> tuple:
        """
        Размер матрицы (строки, столбцы)

        Returns:
            tuple: (строки, столбцы)

        """
        return self.rows, self.columns

    @size.setter
    def size(self, new_value: tuple):
        self.rows = new_value[0]
        self.columns = new_value[1]

    @property
    def rows(self) -> int:
        """
        Количество строк в матрице

        Returns:
            int: количество строк в матрице

        """
        return len(self.matrix)

    @rows.setter
    def rows(self, new_value: int):
        while self.rows < new_value:
            self.append_row([0 for col_no in self.r_cols])
        while self.rows > new_value:
            self.pop_row(self.rows - 1)

    @property
    def columns(self) -> int:
        """
        Количество столбцов в матрице

        Returns:
            int: количество столбцов в матрице

        """
        try:
            return len(self.matrix[0])
        except IndexError:
            return 0

    @columns.setter
    def columns(self, new_value: int):
        while self.columns < new_value:
            self.append_column([0 for col_no in self.r_rows])
        while self.columns > new_value:
            self.pop_column(self.columns - 1)

    @property
    def is_square(self) -> bool:
        """
        Проверяет, является ли матрица квадратной

        Returns:
            bool: является ли матрица квадратной

        """
        return self.columns == self.rows

    @property
    def is_triple_diagonal(self) -> bool:
        """
        Является ли матрица трехдиагональной

        Returns:
            bool: является ли матрица трехдиагональной

        """
        if not self.is_square:
            return False
        for row_no, col_no in self:
            if not (row_no == col_no or row_no - 1 == col_no or row_no == col_no - 1):
                if self[row_no][col_no] != 0:
                    return False
        else:
            return True

    @property
    def is_symmetrical(self) -> bool:
        """
        Проверка на симметриюотносительно главной диагонали

        Returns:
            bool: является ли матрица симметричной относительно главной диагонали

        """
        if not self.is_square:
            raise IndexError("Симметричной можетбыть только квадратная матрица")
        for row_no, col_no in self:
            if self[row_no][col_no] != self[col_no][row_no]:
                return False
        else:
            return True

    @property
    def is_vector(self) -> bool:
        """
        Проверяет является ли объект вектором

        Returns:
            bool: является ли объект вектором

        """
        return 1 in self.size

    @property
    def r_rows(self) -> range:
        """
        Returns:
            range: range(self.rows)

        """
        return range(self.rows)

    @property
    def r_cols(self) -> range:
        """
        Returns:
            range: range(self.columns)

        """
        return range(self.columns)

    @property
    def to_list(self) -> list:
        """
        Returns:
            list: матрица, преобразованная к двумерному списку, вектор к одномерному
        """
        if self.is_vector:
            return self.vector_to_list
        else:
            return self.matrix

    @property
    def multistring(self):
        """
        Returns:
            MultiString: мультистрока матрицы
        """
        return MultiString(self.to_pretty_string())

    @staticmethod
    def wrap(*args, **kwargs):
        """
        Возвращает новую матрицу, не меняя исходную

        Returns:
            Matrix: новая матрица

        """
        return Matrix(*args, **kwargs)

    @staticmethod
    def vector_get_norm_3_vector(size_of_vector):
        """
        Возвращает нормированный вектор нужного размера (по 3 норме)

        Returns:
            Matrix: нормированный вектор нужного размера

        """
        return Matrix([[1 / size_of_vector ** .5 for _ in range(size_of_vector)]])

    @staticmethod
    def load_from_file(filename: str):
        """
        Загружает матрицу из файла

        Args:
            filename (str): имя файла

        Returns:
            Matrix: новая матрица

        """
        with open(filename + '.matrix', 'rb') as file:
            return Matrix(pickle.load(file))


def solve(matrix: (list, Matrix), free_column: (list, Matrix)) -> list:
    """Решение СЛАУ оптимальным методом"""
    if isinstance(matrix, list):
        matrix = Matrix(matrix)
    if isinstance(free_column, Matrix):
        free_column = free_column.vector_to_list
    solution = None
    if matrix.is_triple_diagonal:
        decision = triple(matrix, free_column)
    else:
        # TODO: разобраться в причине неработоспособности метода Гаусса
        # decision = gauss.gauss_method(matrix, free_column)
        """Done"""
        decision = kramer(matrix, free_column)
    for step in decision:
        solution = step.get('Решение')
    return solution
