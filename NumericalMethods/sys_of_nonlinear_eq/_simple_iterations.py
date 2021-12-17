from NumericalMethods import Matrix
from NumericalMethods.util.sympy_init import *


def simple_iterations(system, variables, approximation, transformed_system=None,
                      accuracy_order=8, level_of_details=3, iterations=None):
    raise Exception("Этот метод временно недоступен")
    # TODO: узнать откуда комплексные числа
    def transform(solutions):
        solutions = list(map(simplify, solutions))
        min_sol = solutions[0]
        min_len = len(str(min_sol))
        for solution in solutions:
            if len(str(solution)) < min_len:
                min_sol = solution
                min_len = len(str(min_sol))
        return min_sol

    def calc_delta(old_subs, nw_subs):
        return sum(((elem1 - elem2) ** 2 for elem1, elem2 in zip(old_subs.values(), nw_subs.values()))) ** .5

    def stop_iteration():
        return all([
            delta < 10 ** (-accuracy_order),
            (iteration_counter >= iterations) if iterations is not None else True
        ])

    system = parse_list(system)
    variables = parse_list(variables)
    if transformed_system is None:
        transformed_system = {}
        for var_no in reversed(range(len(variables))):
            transformed_system.update({variables[::-1][var_no]: transform(solve(system[var_no],
                                                                                variables[::-1][var_no]))})
    else:
        new_transformed = {}
        for key in transformed_system:
            new_transformed.update({parse_expr(key): simplify(parse_expr(transformed_system[key]))})
        transformed_system = new_transformed.copy()
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Система': Matrix(system).T,
            'Начальное приближение': approximation,
            'Преобразованная система': transformed_system,
        }
    for_subs = {}
    for var_no in range(len(variables)):
        for_subs.update({variables[var_no]: approximation[var_no]})
    new_subs = {}
    iteration_counter = 1
    while True:
        for key in transformed_system:
            new_subs.update({key: transformed_system[key].evalf(subs=for_subs)})
        delta = calc_delta(for_subs, new_subs)
        for_subs.update(new_subs)
        if level_of_details < 3:
            answer = {
                'Номер итерации': iteration_counter,
                'd': delta
            }
            answer.update(for_subs)
            yield answer
        if stop_iteration():
            if level_of_details < 4:
                yield {'Решение': new_subs}
            break
        iteration_counter += 1


def zeidel_method(system, variables, approximation, transformed_system=None,
                  accuracy_order=8, level_of_details=3, iterations=None):
    raise Exception("Этот метод временно недоступен")
    # TODO: узнать откуда комплексные числа
    def transform(solutions):
        solutions = list(map(simplify, solutions))
        min_sol = solutions[0]
        min_len = len(str(min_sol))
        for solution in solutions:
            if len(str(solution)) < min_len:
                min_sol = solution
                min_len = len(str(min_sol))
        return min_sol

    def calc_delta(old_subs, nw_subs):
        return sum(((elem1 - elem2) ** 2 for elem1, elem2 in zip(old_subs.values(), nw_subs.values()))) ** .5

    def stop_iteration():
        return all([
            delta < 10 ** (-accuracy_order),
            (iteration_counter >= iterations) if iterations is not None else True
        ])

    system = parse_list(system)
    variables = parse_list(variables)
    if transformed_system is None:
        transformed_system = {}
        for var_no in reversed(range(len(variables))):
            transformed_system.update({variables[::-1][var_no]: transform(solve(system[var_no],
                                                                                variables[::-1][var_no]))})
    else:
        new_transformed = {}
        for key in transformed_system:
            new_transformed.update({parse_expr(key): simplify(parse_expr(transformed_system[key]))})
        transformed_system = new_transformed.copy()
    if level_of_details < 3:
        yield {
            'Этап': 'Получены значения',
            'Система': Matrix(system).T,
            'Начальное приближение': approximation,
            'Преобразованная система': transformed_system,
        }
    for_subs = {}
    for var_no in range(len(variables)):
        for_subs.update({variables[var_no]: approximation[var_no]})
    old_subs = for_subs.copy()
    iteration_counter = 1
    while True:
        for key in transformed_system:
            for_subs.update({key: transformed_system[key].evalf(subs=for_subs)})
        delta = calc_delta(old_subs, for_subs)
        old_subs = for_subs.copy()
        if level_of_details < 3:
            answer = {
                'Номер итерации': iteration_counter,
                'd': delta
            }
            answer.update(for_subs)
            yield answer
        if stop_iteration():
            if level_of_details < 4:
                yield {'Решение': for_subs}
            break
        iteration_counter += 1
