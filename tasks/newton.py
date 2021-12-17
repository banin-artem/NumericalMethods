import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods.sys_of_nonlinear_eq import linearization, simple_iterations
from NumericalMethods import Matrix

# ==========================================================================================================
# Нахождение решения системы нелинейных уравнений методом Ньютона (линеаризации), Зейделя и простых итераций
# ==========================================================================================================


def main():
    # Переменные, для которых требуется решение (порядок имеет значение) (должны быть буквы)
    variables = ['x', 'y']

    # Система уравнений
    system = [
        '4 * x * x * x - 2 * y * y * y + 11',
        'x * y - y - 23'
    ]

    # Начальное приближение
    init_approx = (-3, -4)
    # init_approx = (4, 6)

    transformed_system = None
    # Пример ручного преобразования системы (оставить # в началах строк для автоматического преобразования)
    # transformed_system = {
    #     'x': 'sqrt(y)',
    #     'y': 'sqrt(4 - x ** 2)'
    # }

    # ============================================================
    # ВНИМАНИЕ! Пугливым ниже не смотреть! Дальше программный код!
    # ATTENTION!  Not for timid people! Below is the program code!
    # ============================================================

    print(' Решение методом Ньютона (линеаризации) '.center(100, '='))
    decision = linearization(system, variables, init_approx,
                             accuracy_order=8, level_of_details=2, iterations=5)
    for step in decision:
        for info in step:
            if isinstance(step[info], Matrix):
                print(f'{info}:\n')
                step[info].console_display()
            elif isinstance(step[info], dict):
                for key in step[info]:
                    print(f'{key}: {round(step[info][key], 8)}', end='; ')
                print()
            else:
                print(f'{info}: {round(step[info], 8) if isinstance(step[info], float) else step[info]}')
        print()

    print(' Решение методом простых итераций '.center(100, '='))
    decision = simple_iterations(system, variables, init_approx, transformed_system=transformed_system,
                                 level_of_details=2, accuracy_order=8, iterations=5)
    for step in decision:
        step_info = ''
        for info in step:
            if isinstance(step[info], Matrix):
                print(info, ':')
                step[info].console_display()
            else:
                try:
                    step_info += f'{info}: {round(step[info], 8)}'.center(25) + '|'
                except TypeError:
                    step_info += f'{info}: {step[info]}\n'
        print(step_info)


if __name__ == '__main__':
    # Файлы task_%.py сделаны для людей, для которых установка интерпретатора может стать испытанием.
    # Запускают эти люди двойными кликом. А если перед ними консоль будет мгновенно закрываться в случае ошибки,
    # это будет жуткий стресс, а я даже помочь быстро не смогу, а так хоть print ошибки есть.
    try:
        main()
    except Exception as error:
        print(error)
    input('Нажмите "Enter" чтобы выйти...')
