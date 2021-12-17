import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods.util.sympy_init import *
from NumericalMethods.integration import runge_refinement, simpson, trapezoid
from NumericalMethods import Matrix


# ====================================================
#  Численное  интегрирование  по  формуле  трапеций,
# формула Симпсона, уточнение по формуле Рунге-Роберта
# ====================================================


def main():
    function = 'x/(2*x+5)'  # интегрируемая функция
    section = (-1, 1)  # пределы интегрирования
    numbers_of_steps = 4, 8  # количество шагов

    # ============================================================
    # ВНИМАНИЕ! Пугливым ниже не смотреть! Дальше программный код!
    # ATTENTION!  Not for timid people! Below is the program code!
    # ============================================================

    def print_data(data):
        step_info = ''
        for info in data:
            if isinstance(data[info], (tuple, list)):
                step_info += f'{info}: {list(map(lambda val: round(float(val), 8), step[info]))}\n'
            elif isinstance(data[info], float):
                step_info += f'{info}: {round(data[info], 8)}\n'
            elif isinstance(data[info], Matrix):
                print(info)
                data[info].map(float).console_display()
                continue
            else:
                step_info += f'{info}: {data[info]}\n'
        print(step_info)

    print(' Численное интегрирование по формуле трапеций '.center(75, '='))
    for_check_steps = []
    for_check_results = []
    for steps_num in numbers_of_steps:
        decision = trapezoid(function, section, steps_num, level_of_details=1)
        for step in decision:
            if 'Величина шага (h)' in step:
                for_check_steps.append(step['Величина шага (h)'])
            if 'Решение' in step:
                for_check_results.append(step['Решение'])
            print_data(step)
    print(' Уточнение полученных результатов по формуле Рунге-Роберта '.center(75, '='))
    decision = runge_refinement(for_check_results, for_check_steps, level_of_details=2)
    for step in decision:
        print_data(step)

    print(' Численное интегрирование по формуле Симпсона '.center(75, '='))
    for_check_steps = []
    for_check_results = []
    for steps_num in numbers_of_steps:
        decision = simpson(function, section, steps_num, level_of_details=1)
        for step in decision:
            if 'Величина шага (h)' in step:
                for_check_steps.append(step['Величина шага (h)'])
            if 'Решение' in step:
                for_check_results.append(step['Решение'])
            print_data(step)
    print(' Уточнение полученных результатов по формуле Рунге-Роберта '.center(75, '='))
    decision = runge_refinement(for_check_results, for_check_steps, level_of_details=2)
    for step in decision:
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
