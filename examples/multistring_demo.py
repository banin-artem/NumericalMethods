from python_code.main import Matrix


matrix_a = Matrix(2)
matrix_b = Matrix(4)
matrix_a.fill_symbols()
matrix_b.fill_symbols('b')

print('\n', ' сложение мультистрок '.center(75, '='))
print(matrix_a.multistring + matrix_b.multistring)

print('\n', ' сложение c правым разделителем к левой строке '.center(75, '='))
print(matrix_a.multistring.add_r_separator() + matrix_b.multistring)

print('\n', ' сложение c левым разделителем к правой строке '.center(75, '='))
print(matrix_a.multistring + matrix_b.multistring.add_l_separator())

print('\n', ' сложение с автоматическим разделителем '.center(75, '='))
print(matrix_a.multistring.add_with_separator(matrix_b.multistring))

print('\n', ' сложение с автоматическим разделителем и кастомным fillchar '.center(75, '='))
print(matrix_a.multistring.add_with_separator(matrix_b.multistring, '|=|', 20))
