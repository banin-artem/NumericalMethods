from NumericalMethods.util.sympy_init import *


def tangent(function, section, accuracy_order=8, iterations=None, level_of_details=3):
    """
    Решение трансцендентного уравнения методом касательных (Ньютона)

    Args:
        function (str): уравнение в виде строки
        section (tuple): отрезок, на котором будет произведен поиск
        accuracy_order (int): необходимая точность
        iterations (int): необходимое количество итераций
        level_of_details (int): необходимы уровень детализации решения

    Yields:
        dict: информация о текущем шаге решения
    """

    def draw_tangent():
        return value - function(value) / function_d(value)

    def stop_iteration():
        if iteration_counter > (100 if iterations is None else iterations * 10):
            raise IndexError(f"\nОбнаружено нарушение работы функции. Работа аварийно остановлена. Сводка:\n"
                             f"abs(f(x)): {abs(function(value))} < {10 ** (-accuracy_order)} "
                             f"-> {abs(function(value)) < 10 ** (-accuracy_order)}\n"
                             f"abs(old_x - x): {abs(old_value - value)} < {10 ** (-accuracy_order)} -> "
                             f"{abs(function(value)) < 10 ** (-accuracy_order)}\n"
                             f"i: {iteration_counter} >= {iterations} -> "
                             f"{iteration_counter >= 0 if iterations is None else iterations}\n"
                             f"Для нормальной остановки требуется, чтобы все значения были True")
        return all([
            True if accuracy_order is None else abs(function(value)) < 10 ** (-accuracy_order),
            True if accuracy_order is None else abs(old_value - value) < 10 ** (-accuracy_order),
            True if iterations is None else iteration_counter >= iterations,
        ])

    left_edge = min(section)
    right_edge = max(section)
    function = parse_expr(function)
    function = simplify(function)
    function_d = diff(function)
    function_dd = diff(function_d)
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Отрезок': (left_edge, right_edge),
            'Введенная функция': function,
            'Красиво введенная функция': pretty(function, use_unicode=False),
            'Ее производная': function_d,
            'Красиво ее производная': pretty(function_d, use_unicode=False),
            'Ее вторая производная': function_dd,
            'Красиво ее вторая производная': pretty(function_dd, use_unicode=False),
        }
    function = lambdify(x, function)
    function_d = lambdify(x, function_d)
    function_dd = lambdify(x, function_dd)
    if function(right_edge) * function_dd(right_edge) > 0:
        value = right_edge
    else:
        value = left_edge
    iteration_counter = 1
    answer = {}
    while True:
        if level_of_details < 3:
            answer.update({
                'Номер итерации': iteration_counter,
                'a_n-1': value,
                'f(a_n-1)': function(value),
                'f\'(a_n-1)': function_d(value),
                "f''(a_n-1)": function_dd(value)
            })
        old_value = value
        value = draw_tangent()
        if level_of_details < 3:
            answer.update({'a_n': value})
            yield answer
            answer.pop('Номер итерации', None)
            answer.pop('a_n-1', None)
            answer.pop('f(a_n-1)', None)
            answer.pop('f\'(a_n-1)', None)
            answer.pop("f''(a_n-1)", None)
            answer.pop('a_n', None)
        if stop_iteration():
            if level_of_details < 4:
                answer.update({'Решение': value})
            yield answer
            break
        iteration_counter += 1
