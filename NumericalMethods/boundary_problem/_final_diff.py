import re

from NumericalMethods.util.filling_triple import fill_triple_from_lists
from NumericalMethods.first_problem_direct import triple
from NumericalMethods.util.sympy_init import *


def final_difference(equation: str, boundaries_conditions: list,
                     boundaries_in: dict = None, boundary_x: tuple = None,
                     num_of_sections: int = 4, section_step: float = None,
                     level_of_detail: int = 3):
    """
    Решение краевой задачи для ОДУ методом конечных разностей

    Args:
        boundaries_conditions (list): раевые условия (список строк)
        equation (str): уравнение
        boundaries_in (dict): краевые условия
        boundary_x (tuple): краевые иксы (2 значения)
        num_of_sections (int): количество отрезков
        section_step (float): шаг (имеет приоритет над num_of_sections)
        level_of_detail (int): уровень детализации

    Yields:
        dict: значения шага решения

    """

    if boundaries_in is None:
        boundaries_in = dict()
    if boundary_x is None:
        boundary_x = [None, None]

    def get_boundaries(expression, bound_conditions):
        # поиск краевых условий через регулярные выражения (K и L и M)
        regexp = "(?:(?P<K>.*y'{2})|(?P<L>.*y'{1})|(?P<M>.*y))"
        group_names = list('KLM')
        left, right = expression.split('=')
        out = {'F': parse_expr(right)}
        for match in re.finditer(regexp, left):
            for name in group_names:
                if match.group(name):
                    out.update({name: parse_expr(match.group(name).replace("'", '')).subs({y: 1})})

        section = [None, None]
        # поиск краевых условий через регулярные выражения (S и R) I - край отрезка
        regexp = r"(?P<S>[a-zA-Z0-9 \+\-\*\/]*y(?!\'))|(?P<R>[a-zA-Z0-9 \+\-\*\/]*y(?=\'))|(?P<I>(?<=\().+?(?=\)))"
        group_names = list('SRI')
        left, right = bound_conditions[0].split('=')
        out.update({'T': parse_expr(right)})
        for match in re.finditer(regexp, left):
            for name in group_names:
                if match.group(name):
                    if name == 'I':
                        section[0] = parse_expr(match.group(name))
                    else:
                        out.update({name: parse_expr(match.group(name)).subs({y: 1})})
        # поиск краевых условий через регулярные выражения (W и V) I - край отрезка
        regexp = r"(?P<W>[a-zA-Z0-9 \+\-\*\/]*y(?!\'))|(?P<V>[a-zA-Z0-9 \+\-\*\/]*y(?=\'))|(?P<I>(?<=\().+?(?=\)))"
        group_names = list('WVI')
        left, right = bound_conditions[1].split('=')
        out.update({'Z': parse_expr(right)})
        for match in re.finditer(regexp, left):
            for name in group_names:
                if match.group(name):
                    if name == 'I':
                        section[1] = parse_expr(match.group(name))
                    else:
                        out.update({name: parse_expr(match.group(name)).subs({y: 1})})

        return out, min(section), max(section)

    def get_a_x(x_value):
        return boundaries['K'].evalf(subs={x: x_value}) / section_x_len ** 2 - \
               boundaries['L'].evalf(subs={x: x_value}) / (2 * section_x_len)

    def get_b_x(x_value):
        return -2 * boundaries['K'].evalf(subs={x: x_value}) / (section_x_len ** 2) + \
               boundaries['M'].evalf(subs={x: x_value})

    def get_c_x(x_value):
        return boundaries['K'].evalf(subs={x: x_value}) / section_x_len ** 2 + \
               boundaries['L'].evalf(subs={x: x_value}) / (2 * section_x_len)

    def get_d_x(x_value):
        return boundaries['F'].evalf(subs={x: x_value})

    boundaries, boundary_x[0], boundary_x[1] = get_boundaries(equation, boundaries_conditions)
    boundaries.update({key: parse_expr(str(boundaries_in[key])) for key in boundaries_in})
    if section_step is not None:
        section_x_len = section_step
        num_of_sections = int((boundary_x[1] - boundary_x[0]) / section_x_len)
    else:
        section_x_len = (boundary_x[1] - boundary_x[0]) / num_of_sections  # h

    if level_of_detail < 3:
        yield {
            'Выражение': equation,
            'h': section_x_len,
            **boundaries
        }

    points_x = [boundary_x[0] + section * section_x_len for section in range(num_of_sections + 1)]

    diagonal_a = [get_a_x(value) for value in points_x]
    diagonal_b = [get_b_x(value) for value in points_x]
    diagonal_c = [get_c_x(value) for value in points_x]
    free_col_d = [get_d_x(value) for value in points_x]

    diagonal_a.pop(0)
    diagonal_b[0] = -boundaries['R'] / section_x_len + boundaries['S']
    diagonal_c[0] = boundaries['R'] / section_x_len
    free_col_d[0] = boundaries['T']
    free_col_d[-1] = -boundaries['Z']
    diagonal_a[-1] = boundaries['V'] / section_x_len
    diagonal_b[-1] = -boundaries['V'] / section_x_len - boundaries['W']
    diagonal_c.pop(-1)

    free_col_d = list(map(float, free_col_d))

    if level_of_detail < 3:
        yield {
            'Список значений c': diagonal_c,
            'Список значений b': diagonal_b,
            'Список значений a': diagonal_a,
            'Список значений d': free_col_d,
        }

    matrix = fill_triple_from_lists(diagonal_c,
                                    diagonal_b,
                                    diagonal_a).map(lambda val: val if isinstance(val, int) else float(val))

    if level_of_detail < 3:
        drop_matrix = matrix.copy()
        drop_matrix.append_column(free_col_d)
        yield {
            'Матрица': drop_matrix
        }

    decision = triple(matrix, free_col_d, level_of_detail=level_of_detail)
    solution = None
    for step in decision:
        if level_of_detail < 3 and not 'Решение' in step:
            yield step
        solution = step.get('Решение')
    solution = list(map(float, solution))
    if level_of_detail < 4:
        yield {
            'Решение': {
                'X': points_x,
                'Y': solution
            }
        }
