from NumericalMethods.util.sympy_init import *


def simpson(function, section, number_of_steps, level_of_details=3):
    function = parse_expr(function)
    step = (section[1] - section[0]) / number_of_steps
    if level_of_details < 3:
        yield {
            'Этап': 'Приняты значения',
            'Функция': function,
            'Пределы интегрирования': section,
            'Количество шагов (n)': number_of_steps,
            'Величина шага (h)': step,
        }
    x_values = []
    y_values = []
    value = section[0]
    while not value > section[1]:
        x_values.append(value)
        y_values.append(function.evalf(subs={x: value}))
        value += step
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения для таблицы',
            'X': x_values,
            'Y': y_values,
        }
    if level_of_details < 2:
        yield {
            'Этап': 'Рассчет формулы 10.2.1',
            'Формула': f'{step / 3} * ({round(float(y_values[0]))} + 4 * '
                       f'({" + ".join(map(lambda val: str(round(float(val), 8)), y_values[1:-1:2]))})'
                       f'+ 2 * ({" + ".join(map(lambda val: str(round(float(val), 8)), y_values[2:-2:2]))})'
                       f' + {round(float(y_values[-1]), 8)})'
        }
    result = (step / 3) * (y_values[0] + 4 * sum(y_values[1:-1:2]) + 2 * sum(y_values[2:-2:2]) + y_values[-1])
    if level_of_details < 4:
        yield {
            'Решение': float(result)
        }
