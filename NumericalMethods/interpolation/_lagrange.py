from NumericalMethods.util.sympy_init import *


def lagrange_polynomial(x_list_of_values, y_list_of_values):
    if len(x_list_of_values) != len(y_list_of_values):
        raise IndexError("Количество занчений X не совпадает с количеством значений Y")
    polynomial = 0
    for i in range(len(y_list_of_values)):
        expr = 1
        for k in range(len(x_list_of_values)):
            if i != k:
                expr *= x - x_list_of_values[k]
                expr /= x_list_of_values[i] - x_list_of_values[k]
        polynomial += expr * y_list_of_values[i]
    return {
        'Полный многочлен': polynomial,
        'Упрощенный многочлен': simplify(polynomial),
        'Функция python': lambdify(x, simplify(polynomial))
    }
