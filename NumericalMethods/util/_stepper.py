def get_solution(decision):
    solution = None
    for step in decision:
        if 'Решение' in step:
            solution = step.get('Решение')
    return solution
