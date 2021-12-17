import timeit

from python_code import *

max_size_of_matrix = 10
number_of_try = 5
overall_results = {
    'Метод обычных миноров целые': [],
    'Метод быстрых миноров целые': [],
    'Метод обычных миноров дробные': [],
    'Метод быстрых миноров дробные': [],
}

print("Старт синтетического теста скорости вычисления определителя с кэшированием и многопоточностью...\n")

for n in range(1, max_size_of_matrix + 1):
    results = {
        'Метод обычных миноров целые': [],
        'Метод быстрых миноров целые': [],
        'Метод обычных миноров дробные': [],
        'Метод быстрых миноров дробные': [],
    }
    for i in range(number_of_try):
        matrix = Matrix(n)
        matrix2 = Matrix(n)
        matrix.fill_random()
        matrix2.fill_random(-10., 10)
        results['Метод обычных миноров целые'].append(
            timeit.timeit(lambda: methods.matrix.determinant.minor_method(matrix), number=1))
        progress = round((number_of_try * (n - 1) + (i + .25)) / (max_size_of_matrix * number_of_try) * 100)
        print(f'\r{progress}% [{("#" * progress).ljust(100, ".")}] Матрицы {n} порядка, {i + .25} попытка', end='    ')
        results['Метод быстрых миноров целые'].append(
            timeit.timeit(lambda: methods.matrix.determinant.fast_minor_method(matrix), number=1))
        progress = round((number_of_try * (n - 1) + (i + .5)) / (max_size_of_matrix * number_of_try) * 100)
        print(f'\r{progress}% [{("#" * progress).ljust(100, ".")}] Матрицы {n} порядка, {i + .5} попытка', end='    ')
        results['Метод обычных миноров дробные'].append(
            timeit.timeit(lambda: methods.matrix.determinant.minor_method(matrix2), number=1))
        progress = round((number_of_try * (n - 1) + (i + .75)) / (max_size_of_matrix * number_of_try) * 100)
        print(f'\r{progress}% [{("#" * progress).ljust(100, ".")}] Матрицы {n} порядка, {i + .75} попытка', end='    ')
        results['Метод быстрых миноров дробные'].append(
            timeit.timeit(lambda: methods.matrix.determinant.fast_minor_method(matrix2), number=1))
        progress = round((number_of_try * (n - 1) + (i + 1)) / (max_size_of_matrix * number_of_try) * 100)
        print(f'\r{progress}% [{("#" * progress).ljust(100, ".")}] Матрицы {n} порядка, {i + 1} попытка', end='    ')
    for key in results.keys():
        overall_results[key].append(sum(results[key]) / number_of_try)

print('\n\n\nИтоги (чем менше баллов, тем лучше):\n')
for key in overall_results.keys():
    overall_results[key] = [round((elem / (overall_results[key].index(elem) + 1)) * 10 ** 5, 8)
                            for elem in overall_results[key]]
    print(f'{key}: {overall_results[key]}')

print('\nОбщая оценка (чем менше баллов, тем лучше):\n')
for key in overall_results.keys():
    print(f'{key}: {sum(overall_results[key]) / len(overall_results[key])}')

print('\n\nРейтинг методов (чем менше баллов, тем лучше):\n')
rating = []
for key in overall_results.keys():
    rating.append([key, sum(overall_results[key]) / len(overall_results[key])])
rating.sort(key=lambda x: x[1])
for item in rating:
    print(f'{item[0]}: {item[1]}')

# input('\nНажмите "Enter" чтобы выйти...')
