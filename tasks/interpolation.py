import sys
import os
sys.path.append(os.path.pardir)

from NumericalMethods.interpolation import lagrange_polynomial, canonical_polynomial

# =================================================================================
# Нахождение интерполяция методами Лагранжа, Ньютона и через канонический многочлен
# =================================================================================


def main():
    # Таблица для метода Лагранжа
    table_for_lagrange = {
        'x': [0.31415926535 ,0.62831853071 ,0.94247779607, 1.25663706144 ],
        'y': [0.30901699437, 0.58778525229 , 0.80901699437,0.95105651629  ],
        'Подставить значения': [0.78539816339 ]
    }

     #TODO: Исправить метод Ньютона!
     #Таблица для метода Ньютона (не работает)
     #table_for_newton = {
    #     'x': [3, 4, 5],
     #    'y': [22, 19, 18],
     #    'Подставить значения': [3.5]
    # }

    # Таблица для канонического многочлена
    table_for_canonical = {
        'x': [2, 3, 4, 5],
        'y': [20, 22, 19, 18],
        'Подставить значения': [3.5],
        'Рисовать график?': 'да'
    }

    # ============================================================
    # ВНИМАНИЕ! Пугливым ниже не смотреть! Дальше программный код!
    # ATTENTION!  Not for timid people! Below is the program code!
    # ============================================================

    print(' Многочлен Лагранжа '.center(100, '='))

    lagrange_result = lagrange_polynomial(table_for_lagrange['x'], table_for_lagrange['y'])
    print(f'Полный многочлен: {lagrange_result["Полный многочлен"]}\n'
          f'Упрощенный многочлен: {lagrange_result["Упрощенный многочлен"]}')
    function = lagrange_result['Функция python']
    for val in table_for_lagrange['Подставить значения']:
        print(f'y({val}) = {round(function(val), 8)}')

    # TODO: Включить метод Ньютона!
    # print(' Многочлен Ньютона '.center(100, '='))
    
     #lagrange_result = newton_pol(table_for_newton['x'], table_for_newton['y'])
    # print(f'Полный многочлен: {lagrange_result["Полный многочлен"]}\n'
    #       f'Упрощенный многочлен: {lagrange_result["Упрощенный многочлен"]}')
     #function = lagrange_result['Функция python']
     #for val in table_for_newton['Подставить значения']:
     #    print(f'y({val}) = {round(function(val), 8)}')

    print(' Канонический многочлен '.center(100, '='))

    canonical_result = canonical_polynomial(table_for_canonical['x'], table_for_canonical['y'])
    print('Матрица:')
    canonical_result['Матрица'].console_display()
    print(f'Столбец свободных членов: {canonical_result["Столбец свободных членов"]}\n')
    print(f'Решение СЛАУ: {canonical_result["Решение СЛАУ"]}')
    print(f'Полином: {canonical_result["Полином"]}\n')
    function = canonical_result['Функция python']
    for val in table_for_canonical['Подставить значения']:
        print(f'y({val}) = {round(function(val), 8)}')
    if table_for_canonical['Рисовать график?'].lower() == 'да':
        print('\n', " Увы, график рисовать я пока не умею ".center(50, '!'))


if __name__ == '__main__':
    # Файлы task_%.py сделаны для людей, для которых установка интерпретатора может стать испытанием.
    # Запускают эти люди двойными кликом. А если перед ними консоль будет мгновенно закрываться в случае ошибки,
    # это будет жуткий стресс, а я даже помочь быстро не смогу, а так хоть print ошибки есть.
    try:
        main()
    except Exception as error:
        print(error)
    input('Нажмите "Enter" чтобы выйти...')
