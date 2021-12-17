from NumericalMethods.util.sympy_init import *
from NumericalMethods import Matrix


def minimal_sqr(table, level_of_details=3):
    """
    Аппроксимация методом наименьших квадратов (квадратичная)

    Args:
        table (list): таблица значений (список из двух списков - x и y)
        level_of_details (int): необходимый уровень детализации

    Yields:
        dict: информация о текущем шаге решения
    """

    def sum_xny(target_list, _power, second_list=None):
        if second_list is None:
            return sum((elem ** _power for elem in target_list))
        else:
            return sum((elem ** _power * elem2 for elem, elem2 in zip(target_list, second_list)))

    def check_len(target_matrix):
        pr_len = len(target_matrix[0])
        for line in target_matrix:
            if pr_len != len(line):
                return False
        return True

    def function(x_):
        return polynomial.evalf(subs={x: x_})

    if not check_len(table):
        raise IndexError("Количество элементов в строках не совпадает")

    s = 3
    system = []
    for j in range(s):
        new_row = []
        for koef_power in range(s):
            power = s - j - koef_power + 1
            if power > 0:
                new_row.append(sum_xny(table[0], power))
            else:
                new_row.append(len(table[0]))
        system.append(new_row)
    free_column = []
    for koef_power in reversed(range(len(system))):
        free_column.append(sum_xny(table[0], koef_power, table[1]))
    if level_of_details < 3:
        yield {
            'Матрица': Matrix(system),
            'Столбец свободных членов': free_column
        }
    koefs = Matrix(system).slau_solve(free_column)
    polynomial = 0
    for koef_power in range(len(koefs)):
        polynomial += x ** koef_power * koefs[::-1][koef_power]
    sqr_nev = 0
    for i in range(len(table[0])):
        sqr_nev += (function(table[0][i]) - table[1][i]) ** 2
    if level_of_details < 4:
        yield {
            'Многочлен': polynomial
        }
    if level_of_details < 3:
        yield {
            'Коэффициенты': koefs,
            'Функция python': function,
            'Квадратическая невязка': sqr_nev
        }
