from python_code.main import Matrix


matrix = Matrix(3)
matrix.fill_sequence()
matrix.console_display()

print('\n', " нахождение определителя ".center(75, '='))
print(matrix.det)

print('\n', " транспонирование ".center(75, '='))
matrix.T.console_display()

print('\n', " матрица алгебраических дополнений ".center(75, '='))
matrix.complements.console_display()

print('\n', " возведение матрицы в степень ".center(75, '='))
(matrix ** 2).console_display()

print('\n', " умножение матрицы на число ".center(75, '='))
(matrix * 2).console_display()

matrix_1 = Matrix(3)
matrix_1.fill_random()
matrix_1.console_display()

print('\n', " нахождение определителя ".center(75, '='))
print(matrix_1.det)

print('\n', " возведение матрицы отрицательную в степень (обратная матрица) ".center(75, '='))
(matrix_1 ** (-1)).console_display()

print('\n', " сложение матриц ".center(75, '='))
(matrix + matrix_1).console_display()

print('\n', " умножение матриц ".center(75, '='))
(matrix * matrix_1).console_display()

print('\n', " деление матриц (умножение на обратную) ".center(75, '='))
(matrix / matrix_1).console_display()

print('\n', " сравнение матриц ".center(75, '='))
print(matrix == matrix_1)

print('\n', " отрицание (умножение на -1) ".center(75, '='))
(-matrix).console_display()

print('\n', " вычитание матриц ".center(75, '='))
(matrix - matrix_1).console_display()

print('\n', " то же самое для символов ".center(75, '='))
matrix.fill_symbols(col_start=1, row_start=1)
matrix.console_display()

print('\n', " матрица алгебраических дополнений ".center(75, '='))
matrix.complements.console_display()

print('\n', " изменение размера ".center(75, '='))
matrix.size = 5, 5
matrix.console_display()

matrix.columns = 3
matrix.console_display()
matrix.rows = 3
matrix.console_display()
