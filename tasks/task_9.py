import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods.interpolation import minimal_sqr
from NumericalMethods.util.sympy_init import *

__author__ = 'simens_green'

# =========================================================
# Аппроксимация методом наименьших квадратов (квадратичная)
# =========================================================


def main():
    # Таблица из задания
    table_for_minimal_sqr = {
        'x': [-1, 0, 1, 2, 3, 4],
        'y': [-0.5, 0, 0.5, 0.86603, 1.0, 0.86603],
        'Подставить значения': [],
        'Построить график?': 'да'
    }

    # ============================================================
    # ВНИМАНИЕ! Пугливым ниже не смотреть! Дальше программный код!
    # ATTENTION!  Not for timid people! Below is the program code!
    # ============================================================
    function = None
    polynomial = None
    print(' Аппроксимация методом минимальных квадратов '.center(100, '='))
    decision = minimal_sqr([table_for_minimal_sqr['x'], table_for_minimal_sqr['y']], level_of_details=2)
    for step in decision:
        for info in step:
            if 'Матрица' in info:
                step[info].console_display()
            elif 'python' in info:
                function = step[info]
                continue
            else:
                print(f"{info}: {step[info]}")
            if 'Многочлен' in info:
                polynomial = step['Многочлен']
        print()

    for val in table_for_minimal_sqr['Подставить значения']:
        print(f'y({val}) = {round(function(val), 8)}')

    if table_for_minimal_sqr['Построить график?'].lower() == 'да':
        plot(polynomial)


if __name__ == '__main__':
    # Файлы task_%.py сделаны для людей, для которых установка интерпретатора может стать испытанием.
    # Запускают эти люди двойными кликом. А если перед ними консоль будет мгновенно закрываться в случае ошибки,
    # это будет жуткий стресс, а я даже помочь быстро не смогу, а так хоть print ошибки есть.
    try:
        main()
    except Exception as error:
        print(error)
    input('Нажмите "Enter" чтобы выйти...')
