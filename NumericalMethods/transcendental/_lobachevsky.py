def lobachevsky(odds: list, await_delta_order=8, level_of_details=3):
    """
    Решение трансцендентного уравнения методом Лобачевского

    Args:
        level_of_details (int): уровень детализации
        await_delta_order (int): ожидаемый порядок точности (8 означает 10 ** (-8))
        odds (list): коэффициенты при x

    Yields:
        dict: информация о текущем шаге решения
    """
    def line_power(line, power):
        return [elem ** power for elem in line]

    def line_div(line, n):
        return [elem / n for elem in line]

    def line_diff(line_1, line_2):
        diff_line = [abs(elem_1 - elem_2) for elem_1, elem_2 in zip(line_1, line_2)]
        return max(diff_line)

    def get_roots(line, iter_no):
        return [(line[_] / line[_ - 1]) ** (1 / 2 ** iter_no) for _ in range(1, len(line))]

    def check_roots(old_odds, prob_roots):
        true_roots_ = []

        def calc_equation(_koefs, _root):
            result = 0
            for koef in _koefs:
                odd_pow = len(_koefs) - _koefs.index(koef) - 1
                result += koef * _root ** odd_pow
            return result

        for root in prob_roots:
            if round(calc_equation(old_odds, root).real, await_delta_order) == 0:
                true_roots_.append(root)
            elif round(calc_equation(old_odds, -root).real, await_delta_order) == 0:
                true_roots_.append(-root)
            # Нет просчета других вариантов корней
        return true_roots_

    odds_container = odds.copy()
    await_delta = 10 ** (-await_delta_order)
    answer = {}
    if level_of_details < 2:
        answer.update({'Этап': 'Получены значения коэффициентов'})
        answer.update({'Значения': odds})
        yield answer
    odds = line_div(odds, odds[0])
    if level_of_details < 2:
        answer.update({'Этап': 'Значения коэффициентов разделены на первый коэффициент'})
        answer.update({'Значения': odds})
        yield answer
    iteration_counter = 0
    roots = [0 for i in range(len(odds) - 1)]
    delta = None
    answer.pop('Этап', None)
    answer.pop('Значения', None)
    while True:
        if level_of_details < 3:
            answer.update({'Номер итерации': iteration_counter})
            answer.update({'Предполагаемые корни': roots})
            answer.update({'Дельта': delta})
            yield answer
        transforms = [line_power(odds, 2)]
        for transform_no in range(1, len(odds) // 2 + 1):
            transform_step = []
            for i in range(len(odds)):
                if i in range(transform_no, len(odds) - transform_no):
                    transform_step.append(2 * (-1) ** transform_no * odds[i - transform_no] * odds[i + transform_no])
                else:
                    transform_step.append(0)
            transforms.append(transform_step)
        if level_of_details < 3:
            answer.update({'Преобразования': transforms})
        for column in range(len(odds)):
            odds[column] = 0
            for transform_no in range(len(transforms)):
                odds[column] += transforms[transform_no][column]
        if level_of_details < 3:
            answer.update({'Сигма': odds})
        iteration_counter += 1
        old_roots = roots.copy()
        roots = get_roots(odds, iteration_counter)
        delta = line_diff(roots, old_roots)
        if delta < await_delta:
            break
    answer.pop('Номер итерации', None)
    answer.pop('Предполагаемые корни', None)
    answer.pop('Дельта', None)
    answer.pop('Преобразования', None)
    answer.pop('Сигма', None)
    if level_of_details < 4:
        answer.update({"Решение": check_roots(odds_container, roots)})
    yield answer
