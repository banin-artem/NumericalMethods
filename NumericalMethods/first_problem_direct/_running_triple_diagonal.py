def triple(matrix, free_column, level_of_detail=3):
    """
    Решает СЛАУ методом Томаса (прогонки)

    Args:
        matrix (Matrix): матрица, относительно которой требуется решение
        free_column (list): столбец свободных членов
        level_of_detail (int): (int): уровень детализации (меньше число - больше деталей)

    Yields:
        dict: данные о текущем шаге решения

    Raises:
        ArithmeticError: если матрица не является трехдиагональной

    """
    # TODO: оптимизация метода прогонки
    def get_element(row, col):
        if 0 < row <= matrix.rows and 0 < col <= matrix.columns - 1:
            return matrix[row - 1][col - 1]
        else:
            return 0

    # в этом методе используется устаревший метод возврата промежуточных значений (чререз update и pop)
    answer = {}
    matrix = matrix.copy()

    if level_of_detail < 2:
        answer.update({'Этап': 'Получены значения'})
        answer.update({'Матрица': matrix})
        answer.update({'Столбец свободных членов': free_column})
        yield answer
    if not matrix.is_triple_diagonal:
        raise ArithmeticError("Метод прогонки работает только с трехдиагональной марицей")
    matrix.append_column(free_column)
    if level_of_detail < 2:
        answer.update({'Этап': 'Расширена матрица'})
        answer.update({'Матрица': matrix})
        answer.update({'Столбец свободных членов': free_column})
        yield answer
    p = [0]
    q = [0]
    # Прямой ход прогонки
    answer.pop('Этап', None)
    answer.pop('Матрица', None)
    answer.pop('Столбец свободных членов', None)
    if level_of_detail < 3:
        answer.update({'Прямая прогонка': '0 строка'})
        answer.update({'P0': p[0]})
        answer.update({'Q0': q[0]})
        yield answer
        answer.pop('Q0', None)
        answer.pop('P0', None)
    for row_no in range(1, matrix.rows + 1):
        if level_of_detail < 3:
            answer.update({'Прямая прогонка': f'{row_no} строка'})
        a = get_element(row_no, row_no - 1)
        b = get_element(row_no, row_no)
        c = get_element(row_no, row_no + 1)
        d = matrix[row_no - 1][matrix.columns - 1]
        new_p = -c / (b + a * p[row_no - 1])
        if level_of_detail < 2:
            answer.update({'a': a})
            answer.update({'b': b})
            answer.update({'c': c})
            answer.update({'d': d})
            answer.update({"Этап решения": f'P{row_no} = -c / (b + a * P{row_no - 1}) = '
                                           f'P{row_no} = {-c} / ({b} + {a} * {p[row_no - 1]}) = '
                                           f'{new_p}'})
        if level_of_detail < 3:
            answer.update({f'P{row_no}': new_p})
        p.append(new_p)
        new_q = (d - a * q[row_no - 1]) / (b + a * p[row_no if row_no < 2 else row_no - 1])
        if level_of_detail < 2:
            answer.update({"Этап решения": f'Q{row_no} = (d - a * Q{row_no - 1}) / '
                                           f'(b + a * P{row_no if row_no < 2 else row_no - 1}) = '
                                           f'({d} - {a} * {q[row_no - 1]}) / '
                                           f'({b} + {a} * {p[row_no if row_no < 2 else row_no - 1]}) = '
                                           f'{new_q}'})
        if level_of_detail < 3:
            answer.update({f'Q{row_no}': new_q})
        q.append(new_q)
        if level_of_detail < 3:
            yield answer
            answer.pop(f'Q{row_no}', None)
            answer.pop(f'P{row_no}', None)
    # Обратный ход прогонки
    answer.pop('a', None)
    answer.pop('b', None)
    answer.pop('c', None)
    answer.pop('d', None)
    answer.pop('Этап решения', None)
    answer.pop('Прямая прогонка', None)
    x = [0 for row_no in range(matrix.rows + 1)]
    for row_no in range(matrix.rows, 0, -1):
        if level_of_detail < 3:
            answer.update({'Обратная прогонка': f'{row_no} строка'})
        if row_no == matrix.rows:
            if level_of_detail < 2:
                answer.update({f'Этап решения': f"X{row_no} = Q{row_no} = {q[row_no]}"})
            x[row_no] = q[row_no]
        else:
            # Этот if необходим из-за "кривых" индексов
            x[row_no] = q[row_no] + p[row_no] * x[row_no + 1]
            if level_of_detail < 2:
                answer.update({f'Этап решения': f"X{row_no} = Q{row_no} + P{row_no} * X{row_no + 1} = "
                                                f"{q[row_no]} + {p[row_no]} * {x[row_no + 1]} = {x[row_no]}"})
        if level_of_detail < 3:
            answer.update({f"X{row_no}": x[row_no]})
            yield answer
    answer.pop('Этап решения', None)
    answer.pop('Обратная прогонка', None)
    for _ in range(1, len(x)):
        answer.pop(f'X{_}', None)
    if level_of_detail < 4:
        answer.update({'Решение': x[1:]})
    yield answer
