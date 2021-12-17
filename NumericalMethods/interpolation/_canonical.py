from NumericalMethods import Matrix
from NumericalMethods.util.sympy_init import *


def canonical_polynomial(x_list_of_values, y_list_of_values):
    if len(x_list_of_values) != len(y_list_of_values):
        raise IndexError("Количество занчений X не совпадает с количеством значений Y")
    matrix = []
    for row_no in range(len(x_list_of_values)):
        row = []
        for i in range(len(x_list_of_values) - 1, 0, -1):
            row.append(x_list_of_values[row_no] ** i)
        row.append(1)
        matrix.append(row)
    matrix = Matrix(matrix)
    # решение СЛАУ относительно сгененрированной матрицы и столбца свободных членов
    koefs = matrix.slau_solve(y_list_of_values)
    polynomial = 0
    for koef_no in range(len(koefs)):
        polynomial += koefs[::-1][koef_no] * x ** koef_no
    return {
        'Матрица': matrix,
        'Столбец свободных членов': y_list_of_values,
        'Решение СЛАУ': koefs,
        'Полином': polynomial,
        'Функция python': lambdify(x, polynomial)
    }
