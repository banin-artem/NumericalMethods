from NumericalMethods import Matrix


def runge_refinement(results, steps, level_of_details=3):
    if len(results) != len(steps):
        raise IndexError('Количество результатов рассчетов должно совпадать с количеством значений шагов')

    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Результаты': results,
            'Величины шагов': steps
        }

    matrix_first = Matrix(len(results))
    matrix_second = Matrix(len(results))

    for row_no in matrix_first.r_rows:
        matrix_first[row_no][0] = results[row_no]
        matrix_second[row_no][0] = 1

    for row_no in matrix_first.r_rows:
        for col_no in range(1, matrix_first.columns):
            value = steps[row_no] ** (col_no + 1)
            matrix_first[row_no][col_no] = value
            matrix_second[row_no][col_no] = value

    if level_of_details < 3:
        yield {
            'Этап': 'Сформированы матрицы',
            'Первая матрица': matrix_first,
            'Вторая матрица': matrix_second
        }

    first_determinant = matrix_first.det
    second_determinant = matrix_second.det

    if level_of_details < 3:
        yield {
            'Этап': 'Рассчитаны определители',
            'Первый определитель': float(first_determinant),
            'Второй определитель': float(second_determinant)
        }

    if level_of_details < 4:
        yield {
            'Решение': first_determinant / second_determinant
        }
