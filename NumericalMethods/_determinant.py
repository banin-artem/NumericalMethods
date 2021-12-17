from functools import lru_cache


@lru_cache(maxsize=512)
def minor_method(matrix):
    """
    Нахождение определителя по методу миноров (с рекурсией)

    Returns:
        int, float: определитель матрицы

    Raises:
        ArithmeticError: если матрица не является квадратной

    """
    if not matrix.is_square:
        raise ArithmeticError("Определитель возможно найти только у квадратной матрицы")
    matrix = matrix.copy()
    # Точки остановки (в них работает диагональный метод)
    if matrix.rows <= 3:
        return diagonal_method(matrix)
    # Иначе - рекурсия
    else:
        # Но сначала, небольшой бонус от simens_green - ищем строку с наибольшим количеством нулей
        max_zeros_row_no = matrix.search_for_max_num_count(0)
        if matrix[max_zeros_row_no].count(0) == matrix.columns:
            return 0
        det_value = 0
        for row_no in range(matrix.columns):
            # Если значение в ячейке = 0, то пропускаем шаг (избежали потенциальную кучу дополнительных определителей)
            if matrix[max_zeros_row_no][row_no] != 0:
                # Иначе вычисляем через миноры и рекурсию
                if bool((max_zeros_row_no + row_no + 1) % 2):
                    det_value += matrix[max_zeros_row_no][row_no] * auto_det(matrix.minor(max_zeros_row_no, row_no))
                else:
                    det_value -= matrix[max_zeros_row_no][row_no] * auto_det(matrix.minor(max_zeros_row_no, row_no))
        return det_value


@lru_cache(maxsize=512)
def fast_minor_method(matrix):
    """
    Тот же метод миноров, но с предварительной триангуляцией (сокращение до 50% работы метода миноров)
    (метод Гаусса) ТОЧНОСТЬ НИЖЕ, ЧЕМ У МЕТОДА МИНОРОВ

    Returns:
        float: определитель матрицы

    Raises:
        ArithmeticError: если матрица не является квадратной
    """
    matrix = matrix.triangulate()
    return minor_method(matrix)


@lru_cache(maxsize=512)
def diagonal_method(matrix):
    """
    Метод, использующий правило диагоналей, не использует рекурсию

    Returns:
        int, float: определитель матрицы

    Raises:
        ArithmeticError: если матрица не является квадратной
        IndexError: если размерность матрицы больше 3
    """
    if not matrix.is_square:
        raise ArithmeticError("Определитель возможно найти только у квадратной матрицы")
    matrix = matrix.copy()
    if matrix.rows == 1:
        return matrix[0][0]
    elif matrix.rows == 2:
        return matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
    elif matrix.rows == 3:
        return matrix[0][0] * matrix[1][1] * matrix[2][2] + \
               matrix[1][0] * matrix[2][1] * matrix[0][2] + \
               matrix[0][1] * matrix[1][2] * matrix[2][0] - \
               matrix[2][0] * matrix[1][1] * matrix[0][2] - \
               matrix[0][1] * matrix[1][0] * matrix[2][2] - \
               matrix[2][1] * matrix[1][2] * matrix[0][0]
    else:
        raise IndexError("Этот метод не рассчитанн такое")


def auto_det(matrix):
    """
    Автоматический выбор лучшего алгоритма

    Returns:
        int, float: определитель матрицы

    Raises:
        ArithmeticError: если матрица не является квадратной

    """
    if not matrix.is_square:
        raise ArithmeticError("Определитель возможно найти только у квадратной матрицы")
    if matrix.rows > 10:
        return fast_minor_method(matrix)
    else:
        return minor_method(matrix)
