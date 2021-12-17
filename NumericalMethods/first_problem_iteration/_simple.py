def simple(matrix,
           free_column: list,
           await_e: float = None,
           iterations: int = None,
           level_of_detail: int = 3):
    """
    Решает СЛАУ методом простых итераций

    Args:
        matrix (Matrix): матрица, относительно которой требуется решение
        free_column (list): столбец свободных членов
        await_e (float): необходимая точность, например точность до 3 знака после точки - .001
        iterations (int): количество итераций, которое необходимо совершить
        level_of_detail (int): уровень детализации (меньше число - больше деталей)

    Yields:
        dict: данные о текущем шаге решения

    Raises:
        ArithmeticError: если главная диагональ матрицы не является доминирующей

    """
    if iterations is None:
        if await_e is None:
            await_e = (10 ** -8)
    matrix = matrix.copy()
    free_column = free_column.copy()
    answer = {}
    if level_of_detail < 2:
        answer.update({'Этап': 'Получены значения'})
        answer.update({'Матрица': matrix})
        answer.update({'Столбец свободных членов': free_column})
        yield answer
    if not matrix.is_dominant:
        raise ArithmeticError("Метод итераций работает только с матрицами с доминантной диагональю")
    # Извлечение главной диагонали, замещая значения нулями
    new_column = []
    for row_no, col_no in matrix:
        if row_no == col_no:
            new_column.append(matrix[row_no][col_no])
            matrix.matrix[row_no][col_no] = 0
    matrix = -matrix
    # Деление соответствующих строк на значения из диагонали
    for row_no, col_no in matrix:
        matrix.matrix[row_no][col_no] /= new_column[row_no]
    # Деление сободных членов на значения из диагонали
    free_column = [free_elem / diagonal_elem for free_elem, diagonal_elem in zip(free_column, new_column)]
    free_column = matrix.wrap([free_column])
    if level_of_detail < 2:
        answer.update({'Этап': 'Из матрицы извлечена главная диагональ'})
        answer.update({'Матрица': matrix})
        answer.update({'Столбец свободных членов': free_column.matrix[0]})
        yield answer
    # Вычисление нормы (минимальная из двух)
    matrix_norms = (matrix.norma_1, matrix.norma_2)
    vector_norms = (free_column.vector_norma_1, free_column.vector_norma_2)
    norm_number = 1 if matrix.norma_1 <= matrix.norma_2 else 2
    if level_of_detail < 3:
        answer.update({'Этап': 'Вычислены необходимые нормы'})
        answer.update({'Нормы матрицы': matrix_norms})
        answer.update({'Нормы вектора': vector_norms})
        answer.update({'Номер выбранной нормы': norm_number})
        yield answer
    norma_beta = vector_norms[norm_number - 1]
    norma = matrix_norms[norm_number - 1]
    # Принимаем за начальный вектор вектор бета с шапкой
    free_column = free_column.vector_to_list
    solution_vector = free_column.copy()
    # Добавление столбца свободных членов
    matrix.append_column(free_column.copy())
    # Добавление единицы нужно для нормальной работы цикла с матрицей с добавленным столбцом свободных членов
    solution_vector.append(1)
    # Входим в цикл
    delta = None
    epsilon = None
    iteration_counter = 0
    answer.pop('Этап', None)
    answer.pop('Нормы матрицы', None)
    answer.pop('Нормы вектора', None)
    answer.pop('Номер выбранной нормы', None)
    answer.pop('Матрица', None)
    answer.pop('Столбец свободных членов', None)
    while True:
        if level_of_detail < 3:
            answer.update({'Номер итерации': iteration_counter})
            answer.update({'Решение': solution_vector[:-1]})
            answer.update({'Дельта': delta})
            answer.update({'Эпсилон': epsilon})
            yield answer
        if iterations:
            if iteration_counter == iterations:
                break
        elif await_e > (norma ** (iteration_counter - 2)) / (1 - norma) / 10:
            break
        new_solution = []
        for row_no in range(matrix.rows):
            container = 0
            for col_no in range(matrix.columns):
                container += solution_vector[col_no] * matrix[row_no][col_no]
            # Только после заполнения нового вектора (обработана вся матрица), замняем вектор решений на новый на новый
            new_solution.append(container)
        new_solution.append(1)
        iteration_counter += 1
        epsilon = ((norma ** iteration_counter) / (1 - norma)) * norma_beta
        delta = max(map(lambda x: abs(x), [_ - __ for _, __ in zip(solution_vector, new_solution)]))
        # Вот и замена
        solution_vector = new_solution
    answer.pop('Дельта', None)
    answer.pop('Эпсилон', None)
    answer.pop('Номер итерации', None)
    if level_of_detail < 4:
        answer.update({'Решение': solution_vector[:-1]})
    yield answer
