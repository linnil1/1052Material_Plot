from StepFunc import StepFunc
from sympy import degree, LC, symbols


def buildUp(expr, lmax, where):
    x = symbols("x", real=True)
    f = 0
    remain = 0
    while expr != 0:
        add = LC(expr, x) * StepFunc(where, degree(expr, x))
        expr -= add.expand(lim=lmax, func=True)
        remain += add.expand(lim=lmax, func=True)
        f += add
    return f, remain


def buildDown(expr, lmax, where):
    x = symbols("x", real=True)
    f = 0
    while expr != 0:
        cut = -LC(expr, x) * StepFunc(where, degree(expr, x))
        expr += cut.expand(lim=lmax, func=True)
        f += cut
    return f


def buildStep(expr, lmax, exprstart, start, end):
    x = symbols("x", real=True)
    expr = expr.subs({x: exprstart})
    expr, remain = buildUp(expr, lmax, start)
    expr += buildDown(remain, lmax, end)
    return expr
