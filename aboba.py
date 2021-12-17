from math import sin
import numpy as np


def func(x):
    return sin(x) / x

n = 2   # Текущая точность
a = 1
b = 10
Si = []
print("Интегрируемая функция: f(x) = sin(x) / x")
print("Точность: 0.001")


def work(n):
    xi = []     # массив с точками разбиений
    print("Текущее число разбиений", n)
    h = (b - a)/n   # Шаг
    print("Текущий шаг: ", h)
    for x in np.arange(a, b, h):    # заносим в массив xi текущие точки для разбиения
        xi.append(func(x))
    print("Значения выбранных точек: ", xi)
    sum = 0
    for i in xi:
        sum += h * func(i)
    tmp_otvet = h * sum     # вычисление по формуле прямоугольниках
    print("Текущий результат: ", tmp_otvet)
    if n == 2:          # Если запустили в первый раз, то точность не высчитываем
        Si.append(tmp_otvet)    # В список Si скапливаем результаты вычислений
        work(4)     # запускаем рекурсию
    else:
        if abs(Si[-1] - tmp_otvet) < 0.001:     # если необходимая точность достигнута, то выводим ответ
            otvet(tmp_otvet, n)
        else:
            Si.append(tmp_otvet)    # Иначе запускаем рекурсию с увеличенным вдвое числом разбиений
            work(n * 2)


def otvet(S, n):
    print("___________")
    print("Результат: ", S)
    print("Число разбиений: ", n)
    exit(0)

work(2)