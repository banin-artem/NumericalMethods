def __init():
    from sympy import lambdify, diff, simplify, pretty, solve, symbols, evalf, root, pi
    from sympy import Symbol, Pow, Add, Mul, Rational, Float
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.plotting import plot, plot_parametric
    from sympy.abc import x, y


try:
    from ._sympy_init import *
except ModuleNotFoundError:
    try:
        print(f'\n{" Фрагмент программы не найден, устанавливается, это займет поределенное время ".center(100, "!")}',
              end='\n\n')
        import os
        os.system('pip install sympy')
        os.system('pip3 install sympy')
        from ._sympy_init import *
        print(f'\n\n{" Все готово, решаю задание... ".center(100, "=")}\n\n')
    except Exception as error:
        input(str(error))


def find_symbols(expr):
    action_list = [Pow, Add, Mul]
    symbols_list = set()
    for arg in expr.args:
        if isinstance(arg, Symbol):
            symbols_list.update({arg})
        else:
            for action in action_list:
                if isinstance(arg, action):
                    symbols_list.update(find_symbols(arg))
    return symbols_list


def parse_list(target_list):
    return [simplify(parse_expr(target)) for target in target_list]


def extract_complex_root(expr, subs):

    def divide_rational(rational):
        return rational.numerator(), rational.denominator()

    def is_not_odd(number):
        return bool(number % 2)

    def check_root(act):
        for arg_ in act.args:
            if isinstance(arg_, Rational):
                return arg_
        return None

    if isinstance(expr, Pow) and check_root(expr) is not None:
        n, m = divide_rational(check_root(expr))
        if is_not_odd(n) and is_not_odd(m):
            under_root = expr.args[0]
            if under_root.evalf(subs=subs) < 0:
                if n > 0:
                    return -root(abs(under_root) ** n, m)
                else:
                    return 1/-root(abs(under_root) ** -n, m)
            else:
                if n > 0:
                    return root(abs(under_root) ** n, m)
                else:
                    return 1 / root(abs(under_root) ** -n, m)
        else:
            return expr
    else:
        if isinstance(expr, Add):
            out_expr = 0
            for arg in expr.args:
                out_expr += extract_complex_root(arg, subs)
            return out_expr
        elif isinstance(expr, Mul):
            out_expr = 1
            for arg in expr.args:
                out_expr *= extract_complex_root(arg, subs)
            return out_expr
        elif isinstance(expr, Pow):
            out_expr = 1
            for arg in expr.args:
                out_expr **= extract_complex_root(arg, subs)
            return out_expr
        else:
            return expr
