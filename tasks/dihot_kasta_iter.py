import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods.util.sympy_init import Float
from NumericalMethods.transcendental import dichotomy, tangent, secant, iterations

# ==========================================================================
# Нахождение корней уравнения методом дихотомии, хорд, касательных, итераций
# ==========================================================================


# Введите данные из задания
task = {
    'Функция для метода дихотоми': '2*sin(x)-x',
    'Отрезок для метода дихотомии': (1, 3),
    'Функция для метода хорд': 'x * x * x + 9 * x + 5',
    'Отрезок для метода хорд': (0, 2),
    'Функция для метода касательных': 'exp(x)-2*x-2',
    'Отрезок для метода касательных': (1, 2),
    'Функция для метода итераций': '2**x-x**2-0.5',
    # Если вас не устраивает через какое значение был подсчитан результат - укажите два одинаковых
    'Отрезок для метода итераций': (1, 2),
    'x = g(x)': '',
}

# Данные из методички для проверки работы программы (проверьте - значения совпадают)
# task = {
#     'Функция для метода дихотоми': 'x * x - 2',
#     'Отрезок для метода дихотомии': (0, 8),
#     'Функция для метода хорд': 'x * x - 2',
#     'Отрезок для метода хорд': (0, 8),
#     'Функция для метода касательных': 'x * x - 2',
#     'Отрезок для метода касательных': (0, 8),
#     'Функция для метода итераций': 'x ** 3 - x ** 2 + x - 5',
#     'Отрезок для метода итераций': (0, 8),
# }

# ============================================================
# ВНИМАНИЕ! Пугливым ниже не смотреть! Дальше программный код!
# ATTENTION!  Not for timid people! Below is the program code!
# ============================================================


def print_data(data):
    step_info = ''
    for info in data:
        if 'Решение' in data.keys():
            step_info += f'{info}: {round(data[info], 8) if isinstance(data[info], float) else data[info]}\n'
        elif 'Номер итерации' in data.keys():
            value = data[info]
            if isinstance(value, float):
                value = round(value, 8)
            elif isinstance(value, Float):
                value = round(float(value), 8)
            step_info += f'{info}: {value}'.center(23) + '|'
        else:
            step_info += f'{info}:\n{round(data[info], 8) if isinstance(data[info], float) else data[info]}\n'
    if 'Решение' in data.keys():
        print('\n')
    elif 'Номер итерации' in data.keys():
        print(('-' * 23 + '+') * len(data.keys()))
    print(step_info)


def main():
    print(' Решение методом дихотомии '.center(100, '='))
    decision = dichotomy(task['Функция для метода дихотоми'], task['Отрезок для метода дихотомии'],
                         iterations=5, accuracy_order=2, level_of_details=2)
    for step in decision:
        print_data(step)

    print(' Решение методом хорд '.center(100, '='))
    decision = secant(task['Функция для метода хорд'], task['Отрезок для метода хорд'],
                      iterations=5, accuracy_order=3, level_of_details=2)
    for step in decision:
        print_data(step)

    print(' Решение методом касательных '.center(100, '='))
    decision = tangent(task['Функция для метода касательных'], task['Отрезок для метода касательных'],
                       iterations=5, accuracy_order=3, level_of_details=2)
    for step in decision:
        print_data(step)

    print(' Решение методом итераций '.center(100, '='))
    decision = iterations(task['Функция для метода итераций'], task['Отрезок для метода итераций'],
                          task.get('x = g(x)'),
                          level_of_details=2, iterations=5, accuracy_order=3)
    for step in decision:
        if "g'(x)" in step.keys():
            step.update({"g'(x)": None})
        print_data(step)


if __name__ == '__main__':
    # Файлы task_%.py сделаны для людей, для которых установка интерпретатора может стать испытанием.
    # Запускают эти люди двойными кликом. А если перед ними консоль будет мгновенно закрываться в случае ошибки,
    # это будет жуткий стресс, а я даже помочь быстро не смогу, а так хоть print ошибки есть.
    try:
        main()
    except Exception as error:
        print(error)
    input('Нажмите "Enter" чтобы выйти...')

