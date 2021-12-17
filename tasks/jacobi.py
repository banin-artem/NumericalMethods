import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods import Matrix
from NumericalMethods.second_problem import yakobi_rotation

# ==============================================================
# Нахождение собственных чисел и векторов методом вращения Якоби
# ==============================================================


def main():
    # Матрица из задания
    matrix = Matrix([
                     [1, 21, 1],
                     [21, 1, 1],
                     [1, 1, 22]
    ])

    # Количество итераций
    number_of_iterations = 99
    print("Введенная матрица:\n")
    matrix.console_display()

    print("Нахождение собственных чисел и векторов методом вращения Якоби:\n")
    decision = yakobi_rotation(matrix, level_of_detail=2, iterations=number_of_iterations)
    for step in decision:
        for info in step:
            if 'матрица' in info.lower():
                print(info, end=':\n\n')
                step[info].console_display()
            elif info == 'Решение':
                print('\n', ' Решение '.center(75, '='), '\n')
                solution = step['Решение']
                for own_num_no in range(len(solution['Собственные числа'])):
                    print(f'{own_num_no + 1} собственное число: {round(solution["Собственные числа"][own_num_no], 8)}')
                    print(f'{own_num_no + 1} собственный вектор: '
                          f'{[round(_, 8) for _ in solution["Собственные векторы"][own_num_no]]}\n')
            elif info == 'Угол поворота фи':
                print(f'\n{info}: {step[info]}\n')
            else:
                print(f' {info}: {step[info]} '.center(75, '='))


if __name__ == '__main__':
    # Файлы task_%.py сделаны для людей, для которых установка интерпретатора может стать испытанием.
    # Запускают эти люди двойными кликом. А если перед ними консоль будет мгновенно закрываться в случае ошибки,
    # это будет жуткий стресс, а я даже помочь быстро не смогу, а так хоть print ошибки есть.
    try:
        main()
    except Exception as error:
        print(error)
    input('Нажмите "Enter" чтобы выйти...')
