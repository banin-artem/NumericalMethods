def gauss(matrix, free_column: list, level_of_details: int = 3):
    """
    Решает СЛАУ методом Гаусса

    Args:
        matrix (Matrix): матрица, относительно которой требуется решение
        free_column (list): столбец свободных членов
        level_of_details (int): уровень детализации (меньше число - больше деталей)

    Yields:
        dict: данные о текущем шаге решения

    """
    matrix = matrix.copy()
    # Добавляем столбец свободных членов
    matrix.append_column(free_column)
    # Преобразуем матрицу в треугольную с нулями под главной диагональю и единицами в главной диагонали
    matrix = matrix.triangulate_to_ones()
    if level_of_details < 3:
        yield {
            'Этап': 'Закончился первый проход',
            'Матрица': matrix
        }
    solution = [0 for _ in range(matrix.rows)]
    free_column = matrix.pop_column(matrix.columns - 1)
    for row_no in reversed(range(matrix.rows)):
        for col_no in range(matrix.rows):
            free_column[row_no] -= solution[col_no] * matrix.matrix[row_no][col_no]
        solution[row_no] = free_column[row_no]
    if level_of_details < 4:
        yield {
            'Решение': solution
        }
