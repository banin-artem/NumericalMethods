from math import log10, ceil

from NumericalMethods.util.sympy_init import *


def dichotomy(function, section, accuracy_order=None, iterations=None, level_of_details=3):
    """
    Решение трансцендентного уравнения методом дихотомии

    Args:
        function (str): уравнение в виде строки
        section (tuple): отрезок, на котором будет произведен поиск
        accuracy_order (int): необходимая точность
        iterations (int): необходимое количество итераций
        level_of_details (int): необходимы уровень детализации решения

    Yields:
        dict: информация о текущем шаге решения
    """
    def find_center():
        return (right_edge + left_edge) / 2

    def get_section_len():
        return right_edge - left_edge

    def accuracy():
        return ceil(log10(get_section_len() / 2))

    def get_root():
        if accuracy() < 0:
            str_root = str(find_center())
            return float(str_root[:str_root.index('.') + abs(accuracy())])
        else:
            return None

    def stop_iteration():
        if iteration_counter > (100 if iterations is None else iterations * 10):
            raise IndexError(f"\nОбнаружено нарушение работы функции. Работа аварийно остановлена. Сводка:\n"
                             f"abs(f(x)): {abs(accuracy())} < {10 ** (-accuracy_order)} "
                             f"-> {abs(function(accuracy())) < 10 ** (-accuracy_order)}\n"
                             f"abs(old_x - x): {abs(old_center - center)} < {10 ** (-accuracy_order)} -> "
                             f"{abs(old_center - center) < 10 ** (-accuracy_order)}\n"
                             f"i: {iteration_counter} >= {iterations} -> "
                             f"{iteration_counter >= 0 if iterations is None else iterations}\n"
                             f"Для нормальной остановки требуется, чтобы все значения были True")
        return all([
            True if accuracy_order is None else abs(accuracy()) > accuracy_order,
            True if accuracy_order is None else abs(old_center - center) < 10 ** (-accuracy_order),
            True if iterations is None else iteration_counter >= iterations,
        ])

    if accuracy_order is None and iterations is None:
        accuracy_order = 8

    left_edge = min(section)
    right_edge = max(section)
    function = parse_expr(function)
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Отрезок': (left_edge, right_edge),
            'Введенная функция': function,
            'Красиво введенная функция': pretty(function, use_unicode=False),
        }
    function = lambdify(x, function)
    center = find_center()
    old_center = center
    iteration_counter = 1
    while True:
        f_a = function(left_edge)
        f_c = function(center)
        f_b = function(right_edge)
        if level_of_details < 3:
            yield {
                'Номер итерации': iteration_counter,
                'a': left_edge,
                'c': center,
                'b': right_edge,
                'f(a)': f_a,
                'f(c)': f_c,
                'f(b)': f_b
            }
        if stop_iteration():
            if level_of_details < 4:
                yield {'Решение': get_root()}
            if level_of_details < 3:
                yield {
                        'Последний отрезок': (left_edge, right_edge),
                        'Длина последнего отрезка': get_section_len(),
                        'Середина последнего отрезка': find_center()
                    }
            else:
                yield {}
            break
        if f_a * f_c < 0:
            right_edge = center
        else:
            left_edge = center
        old_center = center
        center = find_center()
        iteration_counter += 1
