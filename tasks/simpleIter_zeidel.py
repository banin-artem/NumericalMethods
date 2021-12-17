import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods.first_problem_iteration import zeidel, simple
from NumericalMethods import Matrix

# =======================================================
# Решение СЛАУ методом простых итераций и методом Зейделя
# =======================================================


def main():
    # Матрица из задания
    matrix = Matrix([
         
          [20, 1, 1], 
          [11, 20, 1],
          [1, 1, 20], 
    ])
    # Столбец свободных членов
    free_column = [2, 11, 6]

    print("Введенная матрица:")
    matrix.console_display()

    print(f"Столбец свободных членов: {free_column}\n")

    if not matrix.is_dominant:
        print("Матрица не сходится")
        input('Нажмите "Enter" чтобы выйти...')
        exit()
    else:
        print(f"\n{' Решение методом простых итераций '.center(50, '=')}\n")
        solution = simple(matrix, free_column, iterations=10, level_of_detail=2)
        for step in solution:
            step_info = ''
            for info in step:
                if info not in ['Матрица']:
                    if info in ['Нормы матрицы', 'Нормы вектора', 'Решение']:
                        step_info += f'{info}: {list(map(lambda x: round(x, 8), step[info]))}\n'
                    else:
                        step_info += f'{info}: ' \
                                     f'{step[info] if not isinstance(step[info], float) else round(step[info], 8)}\n'
            print(step_info)

        print(f"\n{' Решение методом Зейделя '.center(50, '=')}\n")
        solution = zeidel(matrix, free_column, iterations=5, level_of_detail=2)
        for step in solution:
            step_info = ''
            for info in step:
                if info not in ['Матрица']:
                    if info in ['Нормы матрицы', 'Нормы вектора', 'Решение']:
                        step_info += f'{info}: {list(map(lambda x: round(x, 8), step[info]))}\n'
                    else:
                        step_info += f'{info}: ' \
                                     f'{step[info] if not isinstance(step[info], float) else round(step[info], 8)}\n'
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
