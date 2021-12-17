from NumericalMethods import Matrix
from NumericalMethods.util.sympy_init import *


def linearization(system, variables, approximation, accuracy_order=8, level_of_details=3, iterations=None):
    """
    Решение СНЛАУ методом линеаризации (Ньютона)

    Args:
        system (list): список строк СНЛАУ
        variables (list): используемые пременные
        approximation (tuple): начальное приближение
        accuracy_order (int): необходимая точность
        level_of_details (int): необходимый уровень детализации
        iterations (int): неоюходимое количество итераций

    Yields:
        dict: информация о текущем шаге решения
    """
    def get_subs(vars_, approx):
        out = {}
        approx = approx.vector_to_list
        for var_no in range(len(vars_)):
            out.update({vars_[var_no]: approx[var_no]})
        return out

    def stop_iteration():
        return all([
            delta < 10 ** (-accuracy_order),
            (iteration_counter >= iterations) if iterations is not None else True,
            system_calc.vector_norma_1 < 10 ** (-accuracy_order)
        ])

    system = parse_list(system)
    variables = parse_list(variables)
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Система уравнений': Matrix(system).T,
            'Использованные переменные': variables,
            'Начальное приближение': approximation
        }
    approximation = Matrix(list(approximation)).T
    matrix_j_n = Matrix(len(system), len(variables))
    for row_no, col_no in matrix_j_n:
        matrix_j_n[row_no][col_no] = diff(system[row_no], variables[col_no])
    if level_of_details < 2:
        yield {
            "Этап": "Получена матрица Якоби",
            'J_n': matrix_j_n
        }
    system = Matrix(system)
    matrix_j_n_rev = (matrix_j_n ** (-1)).map(simplify)
    if level_of_details < 2:
        yield {
            "Этап": "Получена обратная матрица для матрицы Якоби",
            'J_n ** (-1)': matrix_j_n_rev
        }
    iteration_matrix = (matrix_j_n_rev * system).map(simplify)
    if level_of_details < 3:
        yield {
            "Этап": "Вычислена матрица для совершения итераций",
            'J_n ** (-1) * f(n)': iteration_matrix
        }
    evalfed_matrix = Matrix(iteration_matrix.rows, iteration_matrix.columns)
    iteration_counter = 0
    while True:
        system_calc = system.T
        functions = []
        for row_no in iteration_matrix.r_rows:
            evalfed_matrix[row_no][0] = iteration_matrix[row_no][0].evalf(subs=get_subs(variables, approximation))
            system_calc[row_no][0] = system_calc[row_no][0].evalf(subs=get_subs(variables, approximation))
            functions.append(system_calc[row_no][0])
        old_approx = approximation
        if level_of_details < 3:
            yield {
                "Номер итерации": iteration_counter,
                'Решение': get_subs(variables, approximation),
                '||F||_1': system_calc.vector_norma_1,
                'F_1': functions[0],
                'F_2': functions[1]
            }
        approximation -= evalfed_matrix
        delta = (old_approx - approximation).vector_norma_1
        if stop_iteration():
            if level_of_details < 4:
                yield {
                    'Решение': get_subs(variables, approximation)
                }
            break
        iteration_counter += 1
