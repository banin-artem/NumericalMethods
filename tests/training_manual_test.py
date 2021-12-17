import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.pardir))
sys.path.append(os.path.abspath(os.path.pardir) + '/NumericalMethods')

import NumericalMethods.first_problem_iteration as first_problem_iteration
import NumericalMethods.interpolation as interpolation
import NumericalMethods.second_problem as second_problem
import NumericalMethods.sys_of_nonlinear_eq as nonlinear
import NumericalMethods.transcendental as transcendental
from NumericalMethods import Matrix
from NumericalMethods.first_problem_direct import gauss, triple
from NumericalMethods.util import get_solution


def list_round(list_, accuracy=8):
    return list(map(lambda value: round(float(value), accuracy), list_))


# =======================================================
# Первая проблема линейной алгебры. Прямые методы решения
# =======================================================


@pytest.mark.xfail
def test_gauss():
    matrix = Matrix([
        [2, 5, 1],
        [-1, 2, -2],
        [6, 2, 1]
    ])
    free = [1, 2, 3]
    true_solution = [12 / 9, 10 / 57, -65 / 57]

    solution = get_solution(gauss(matrix, free))

    assert list_round(solution) == list_round(true_solution)


def test_reverse_matrix():
    matrix = Matrix([
        [2, 3, 6],
        [3, 6, 2],
        [6, 2, 8],
    ])
    true_solution = Matrix([
        [-11 / 32, 3 / 32, 15 / 64],
        [3 / 32, 5 / 32, -7 / 64],
        [15 / 64, -7 / 64, -3 / 128]
    ])

    solution = matrix ** -1

    assert solution.map(lambda value: round(float(value), 8)) == true_solution.map(lambda value: round(float(value), 8))


def test_triple_solve():
    matrix = Matrix([
        [-34, -26, 0, 0, 0],
        [64, -124, -56, 0, 0],
        [0, 94, -274, -86, 0],
        [0, 0, 124, -484, -116],
        [0, 0, 0, 154, -754]
    ])
    free = [34, 38, 42, 46, 50]
    true_solution = [-.6181818, -.4993007, -.2794706, -.1437131, -.0956655]

    solution = get_solution(triple(matrix, free))

    assert list_round(solution, 7) == list_round(true_solution, 7)


# ==================================================================
# Первая проблема линейной алгебры. Итерационные методы решения СЛАУ
# ==================================================================

def test_first_problem_iteration_simple():
    matrix = Matrix([
        [20, 4, -8],
        [-3, 15, 5],
        [6, 3, -18],
    ])
    free = [1, -2, 3]
    true_solution = [-.0077608, -.0743338, -.1816226]

    solution = get_solution(first_problem_iteration.simple(matrix, free, iterations=7))

    assert list_round(solution, 7) == list_round(true_solution, 7)


def test_first_problem_iteration_zeidel():
    matrix = Matrix([
        [20, 4, -8],
        [-3, 15, 5],
        [6, 3, -18],
    ])
    free = [1, -2, 3]
    true_solution = [-.0077778, -.0743447, -.18165]

    solution = get_solution(first_problem_iteration.zeidel(matrix, free, iterations=5))

    assert list_round(solution, 7) == list_round(true_solution, 7)


# ================================
# Вторая проблема линейной алгебры
# ================================


def test_second_problem_power_method():
    matrix = Matrix([
        [-12, 4, 8],
        [4, 11, -6],
        [8, -6, 2],
    ])
    true_solution = -17

    solution = get_solution(second_problem.power_method(matrix))

    assert round(float(solution)) == true_solution


def test_second_problem_yakobi_rotation():
    matrix = Matrix([
        [17, 1, 1],
        [1, 17, 2],
        [1, 2, 4],
    ])
    true_solution = [16.0349, 18.31907, 3.646025]

    solution = get_solution(second_problem.yakobi_rotation(matrix))['Собственные числа']

    assert list_round(solution, 4) == list_round(true_solution, 4)


# ========================================
# Методы решения трансцендентных уравнений
# ========================================


def test_transcendental_dichotomy():
    task = 'x ** 2 - 2'
    task_section = (0, 8)
    true_solution = 2 ** .5

    solution = get_solution(transcendental.dichotomy(task, task_section, level_of_details=2))

    assert round(float(solution), 8) == round(float(true_solution), 8)


def test_transcendental_secant():
    task = 'x ** 2 - 2'
    task_section = (0, 8)
    true_solution = 2 ** .5

    solution = get_solution(transcendental.secant(task, task_section))

    assert round(float(solution), 8) == round(float(true_solution), 8)


def test_transcendental_tangent():
    task = 'x ** 2 - 2'
    task_section = (0, 8)
    true_solution = 2 ** .5

    solution = get_solution(transcendental.tangent(task, task_section))

    assert round(float(solution), 8) == round(float(true_solution), 8)


def test_transcendental_iterations():
    task = 'x ** 3 - x ** 2 + x - 5'
    task_section = (8, 8)
    true_solution = 1.8814850755

    solution = get_solution(transcendental.iterations(task, task_section,
                                                      level_of_details=2, iterations=8, accuracy_order=1))

    assert round(float(solution), 8) == round(float(true_solution), 8)


# ===================================
# Решение систем нелинейных уравнений
# ===================================


@pytest.mark.xfail
def test_sys_of_nonlinear_eq_linearization():
    variables = ['x', 'y']
    system = [
        'x ** 2 + y ** 2 - 4',
        'x ** 2 - y'
    ]
    init_approx = (2, 2)
    true_solution = [1.2490080305, 1.5663342918]

    solution = get_solution(nonlinear.linearization(system, variables, init_approx, iterations=11))
    solution = list(solution.values())

    assert list_round(solution, 8) == list_round(true_solution, 8)


# ============
# Интерполяция
# ============


@pytest.mark.xfail
def test_interpolation_canonical_polynomial():
    x_values = [-1, 1, 5]
    y_values = [4, -2, 10]
    true_solution = []

    solution = get_solution(interpolation.canonical_polynomial(x_values, y_values))

    assert true_solution == solution
