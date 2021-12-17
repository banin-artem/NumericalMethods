from NumericalMethods import Matrix
from NumericalMethods.first_problem_direct import triple
from NumericalMethods.util.sympy_init import *


def c_spline(x_list, y_list, level_of_detail=3):

    def function(x_value):

        def find_section(value):
            """
            Поиск номера отрезка по значению точки

            Args:
                value: значение точки

            Returns:
                int: номер отрезка
            """
            if value < x_list[0]:
                return 1
            elif value > x_list[-1]:
                return len(x_list) - 1
            else:
                for no in range(1, len(x_list)):
                    if x_list[no - 1] <= value < x_list[no]:
                        return no

        i = find_section(x_value)
        # формула из методички (8.6 на странице 64)
        polynomial = m_list[i] * (x - x_list[i - 1]) ** 3 / (6 * h_list[i]) + \
                     m_list[i - 1] * (x_list[i] - x) ** 3 / (6 * h_list[i]) + \
                     (y_list[i] - m_list[i] * h_list[i] ** 2 / 6) * (x - x_list[1]) / h_list[i] + \
                     (y_list[i - 1] - m_list[i - 1] * h_list[i] ** 2 / 6) * (x_list[i] - x) / h_list[i]
        return polynomial.evalf(subs={x: x_value})

    if len(x_list) != len(y_list):
        raise IndexError("Длины списков x и y не совпадают")

    h_list = [x_list[no + 1] - x_list[no] for no in range(len(x_list) - 1)]
    matrix = [[0 for i in range(len(x_list) - 2)] for j in range(len(x_list) - 2)]
    free_column = []
    # генерация трехдиагональной матрицы (страница 65)
    for row_no in range(len(matrix)):
        for col_no in range(len(matrix[0])):
            if row_no - 1 == col_no:
                matrix[row_no][col_no] = h_list[row_no] / 6
            elif row_no == col_no:
                matrix[row_no][col_no] = (h_list[row_no] + h_list[row_no + 1]) / 3
            elif row_no == col_no - 1:
                matrix[row_no][col_no] = h_list[row_no + 1] / 6
        free_column.append((y_list[row_no + 2] - y_list[row_no + 1]) / h_list[row_no + 1] -
                           (y_list[row_no + 1] - y_list[row_no]) / h_list[row_no])

    matrix = Matrix(matrix)
    if level_of_detail < 3:
        matrix.append_column(free_column)
        yield {
            'Матрица системы (8.7)': matrix
        }
        matrix.pop_column(matrix.columns - 1)
    decision = triple(matrix, free_column, level_of_detail=level_of_detail)
    m_list = None
    for step in decision:
        if 'Решение' not in step.keys():
            yield step
        else:
            m_list = step['Решение']

    m_list.insert(0, 0)
    m_list.append(0)
    h_list.insert(0, None)

    pol_list = []
    for i in range(1, len(m_list)):
        # формула из методички (8.6 на странице 64)
        pol_list.append(simplify(m_list[i] * (x - x_list[i - 1]) ** 3 / (6 * h_list[i]) +
                                 m_list[i - 1] * (x_list[i] - x) ** 3 / (6 * h_list[i]) +
                                 (y_list[i] - m_list[i] * h_list[i] ** 2 / 6) * (x - x_list[1]) / h_list[i] +
                                 (y_list[i - 1] - m_list[i - 1] * h_list[i] ** 2 / 6) * (x_list[i] - x) / h_list[i]))
    yield {
        'Список многочленов': pol_list,
        'Функция Python': function,
    }
