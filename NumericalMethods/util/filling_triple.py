from NumericalMethods._matrix import Matrix


def fill_triple_from_lists(list_up: list, list_middle: list, list_down: list) -> Matrix:
    """
    Заполняет трехдиагональную матрицу, используя 3 списка

    Args:
        list_up (list): список над главной диагональю
        list_middle (list): список главной диагонали
        list_down (list): список под главной диагональю

    Returns:
        Matrix: заполненная трехдиагональная матрица
    """
    out_matrix = Matrix(len(list_middle))

    for row_no, col_no in out_matrix:
        if row_no == col_no - 1:
            out_matrix[row_no][col_no] = list_up[row_no]
        if row_no == col_no:
            out_matrix[row_no][col_no] = list_middle[row_no]
        if row_no - 1 == col_no:
            out_matrix[row_no][col_no] = list_down[col_no]

    return out_matrix
