from NumericalMethods.util.sympy_init import *


def secant(function, section, accuracy_order=None, iterations=None, level_of_details=3):
    """
    Решение трансцендентного уравнения методом хорд

    Args:
        function (str): уравнение в виде строки
        section (tuple): отрезок, на котором будет произведен поиск
        accuracy_order (int): необходимая точность
        iterations (int): необходимое количество итераций
        level_of_details (int): необходимы уровень детализации решения

    Yields:
        dict: информация о текущем шаге решения
    """
    def draw_secant():
        return (left_edge * function(right_edge) - right_edge * function(left_edge)) / \
               (function(right_edge) - function(left_edge))

    def stop_iteration():
        if iteration_counter > (100 if iterations is None else iterations * 10):
            raise IndexError(f"\nОбнаружено нарушение работы функции. Работа аварийно остановлена. Сводка:\n"
                             f"abs(f(x)): {abs(function(suppression))} < {10 ** (-accuracy_order)} "
                             f"-> {abs(function(suppression)) < 10 ** (-accuracy_order)}\n"
                             f"abs(old_x - x): {abs(old_c - suppression)} < {10 ** (-accuracy_order)} -> "
                             f"{abs(function(suppression)) < 10 ** (-accuracy_order)}\n"
                             f"i: {iteration_counter} >= {iterations} -> "
                             f"{iteration_counter >= 0 if iterations is None else iterations}\n"
                             f"Для нормальной остановки требуется, чтобы все значения были True")
        return all([
            True if accuracy_order is None else abs(function(suppression)) < 10 ** (-accuracy_order),
            True if accuracy_order is None else abs(old_c - suppression) < 10 ** (-accuracy_order),
            True if iterations is None else iteration_counter >= iterations,
        ])

    if accuracy_order is None and iterations is None:
        accuracy_order = 8

    left_edge = min(section)
    right_edge = max(section)
    function = parse_expr(function)
    answer = {}
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Отрезок': (left_edge, right_edge),
            'Введенная функция': function,
            'Красиво введенная функция': pretty(function, use_unicode=False)
        }
    function = lambdify(x, function)
    suppression = None
    f_a = function(left_edge)
    f_c = None
    f_b = function(right_edge)
    iteration_counter = 1
    old_c = 0
    while True:
        if level_of_details < 3:
            yield {
                'Номер итерации': iteration_counter,
                'a': left_edge,
                'c': suppression,
                'b': right_edge,
                'f(a)': f_a,
                'f(c)': f_c,
                'f(b)': f_b
            }
        suppression = draw_secant()
        f_c = function(suppression)
        if level_of_details < 3:
            yield {
                'Номер итерации': iteration_counter,
                'a': None,
                'c': suppression,
                'b': None,
                'f(a)': None,
                'f(c)': f_c,
                'f(b)': None
            }
        if stop_iteration():
            if level_of_details < 4:
                answer.update({'Решение': suppression})
            if level_of_details < 3:
                answer.update({'f(c)': f_c})
            yield answer
            break
        old_c = suppression
        if function(left_edge) * function(suppression) > 0:
            left_edge = suppression
            suppression = None
        else:
            right_edge = suppression
            suppression = None
        f_a = function(left_edge)
        f_c = None
        f_b = function(right_edge)
        iteration_counter += 1
