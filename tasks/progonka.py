import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods.first_problem_direct import triple
from NumericalMethods import Matrix
# =============================
# Решение СЛАУ методом прогонки
# =============================


def main():
    # Матрица из задания
    matrix = Matrix([
                     [6, -5, 0, 0, 0],
                     [-6, 16, 9, 0, 0],
                     [0, 9, -17, -3,  0],     
                     [0, 0, 8, 22,  -8],  
                     [0, 0, 0, 6,  -13],  
    ])
    # Столбец свободных членов
    free_column = [-58, 161, -114, -90, -55]
    print(f"Столбец свободных членов: {free_column}\n")

    print("Введенная матрица:\n")
    matrix.console_display()

    print("Решение методом прогонки:\n")
    solution = triple(matrix, free_column, level_of_detail=2)
    for step in solution:
        step_info = ''
        for info in step:
            if info not in ['Матрица']:
                if isinstance(step[info], (tuple, list)):
                    step_info += f'{info}: {list(map(lambda x: round(x, 8), step[info]))}\n'
                elif isinstance(step[info], float):
                    step_info += f'{info}: {round(step[info], 8)}\n'
                else:
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
