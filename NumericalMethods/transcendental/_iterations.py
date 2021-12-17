from NumericalMethods.util.sympy_init import *


def iterations(function, section, g_function=None, accuracy_order=8, iterations=None, level_of_details=3):
    """
    Решение трансцендентного уравнения методом итераций

    Args:
        g_function (str): преобразованное уравнение к виду x=g(x)
        function (str): уравнение в виде строки
        section (tuple): отрезок, на котором будет произведен поиск
        accuracy_order (int): необходимая точность
        iterations (int): необходимое количество итераций
        level_of_details (int): необходимы уровень детализации решения

    Yields:
        dict: информация о текущем шаге решения
    """
    def calc_any(func, number):
        # extract_complex_root облявлена в sympy_init и должна заменять корни нечетной степени
        # в случае, если подкоренное выражение отрицательное, на минус корень из модуля этого выражения
        new_function = extract_complex_root(func, {x: number})
        return new_function.evalf(subs={x: number})

    def calc_function(number):
        return calc_any(function, number)

    def calc_g_function(number):
        return calc_any(g_function, number)

    def calc_g_function_d(number):
        return calc_any(g_function_d, number)

    def stop_iteration():
        if iteration_counter > (100 if iterations is None else iterations * 10):
            raise IndexError(f"\nОбнаружено нарушение работы функции. Работа аварийно остановлена. Сводка:\n"
                             f"abs(f(x)): {abs(function(x_value))} < {10 ** (-accuracy_order)} "
                             f"-> {abs(function(x_value)) < 10 ** (-accuracy_order)}\n"
                             f"abs(old_x - x): {abs(old_x_value - x_value)} < {10 ** (-accuracy_order)} -> "
                             f"{abs(function(x_value)) < 10 ** (-accuracy_order)}\n"
                             f"i: {iteration_counter} >= {iterations} -> {iteration_counter >= iterations}\n"
                             f"Для нормальной остановки требуется, чтобы все значения были True")
        return all([
            True if accuracy_order is None else abs(calc_function(x_value)) < 10 ** (-accuracy_order),
            True if accuracy_order is None else abs(old_x_value - x_value) < 10 ** (-accuracy_order),
            True if iterations is None else iteration_counter >= iterations,
        ])

    left_edge = section[0]
    right_edge = section[1]
    function = simplify(parse_expr(function))
    if g_function is None:
        # если пользователь не преобразовал к нужному виду, совершение попытки автоматического преобразования
        solving = map(simplify, solve(function.subs(x ** 3, y ** 3), y))
        try:
            g_function = solve(function.subs(x**3, y**3), y)[0]
            min_len = len(str(g_function))
            for new_g_function in solving:
                # экспериментально было выявлено, что наилучшее преобразование самое короткое и не содержит комплексных
                # чисел (без 'I')
                if len(str(new_g_function)) < min_len and 'I' not in str(new_g_function):
                    min_len = len(str(new_g_function))
                    g_function = new_g_function
        except IndexError:
            raise IndexError("Вероятно, не был найден способ преобразования функции к виду x = g(x)")
    else:
        g_function = simplify(parse_expr(g_function))
    g_function_d = simplify(diff(g_function))
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Отрезок': (left_edge, right_edge),
            'Введенная функция': function,
            'Красиво введенная функция': pretty(function, use_unicode=False),
            'g(x)': g_function,
            'Красиво g(x)': pretty(g_function, use_unicode=False),
            "g'(x)": g_function_d,
            "Красиво g'(x)": pretty(g_function_d, use_unicode=False)
        }
    iteration_counter = 1
    if abs(calc_g_function_d(left_edge)) < 1:
        x_value = left_edge
    else:
        x_value = right_edge
    if level_of_details < 3:
        yield {
            'Номер итерации': iteration_counter,
            'x': x_value,
            'f(x)': calc_function(x_value),
            'g(x)': calc_g_function(x_value),
            "g'(x)": calc_g_function_d(x_value)
        }
    while True:
        old_x_value = x_value
        x_value = calc_g_function(x_value)
        if stop_iteration():
            if level_of_details < 3:
                yield {'Решение': x_value, }
            else:
                yield {}
            break
        iteration_counter += 1
        if level_of_details < 3:
            yield {
                'Номер итерации': iteration_counter,
                'x': x_value,
                'f(x)': calc_function(x_value),
                'g(x)': calc_g_function(x_value),
                "g'(x)": calc_g_function_d(x_value)
            }
