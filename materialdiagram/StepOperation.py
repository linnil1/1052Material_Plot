from .StepFunc import StepFunc
from sympy import degree, symbols, Add, Mul, factorial, simplify


def taylorExpand(expr, a):
    x = symbols("x", real=True)
    if not expr:
        return []
    return [expr.diff(x, i).subs({x: a}) / factorial(i)
            for i in range(degree(expr, x) + 1)]


def taylorBuild(exparr, a):
    x = symbols("x", real=True)
    return sum(n * (x - a) ** i for i, n in enumerate(exparr))


def taylorBuildStep(expr, a):
    x = symbols("x", real=True)
    exparr = taylorExpand(expr, a)
    return sum(n * StepFunc(x - a, i) for i, n in enumerate(exparr))


def buildStep(expr, lmax, exprstart, start, end):
    x = symbols("x", real=True)
    expr = simplify(expr).subs({x: x - exprstart}).expand(lim=lmax, func=True)
    f = taylorBuildStep(expr, start)
    f -= taylorBuildStep(simplify(f).expand(lim=lmax, func=True), end)
    return f


def weightFill(weight, lmax):
    weight.append((0, lmax, lmax))
    full_wei = []
    st = 0
    for i, wei in enumerate(weight):
        if st != wei[1]:
            full_wei.append((1, st, wei[1]))
        st = wei[2]
        full_wei.append(wei)
        if st == lmax:
            break
    return full_wei


def weightMul(expr, wei, lmax):
    x = symbols("x", real=True)
    wei = weightFill(wei, lmax)
    f = 0
    for term in Add.make_args(expr):
        xfrm = 0
        expterm = term
        for m in Mul.make_args(term):
            if isinstance(m, StepFunc):
                xfrm = x - m.args[0]
                expterm = term.expand(lim=lmax, func=True)
                func = m

        for w in wei:
            # outside range
            if w[2] <= xfrm:
                continue
            # partical inside range
            elif w[1] <= xfrm <= w[2]:
                f += buildStep(expterm * w[0],
                               lmax, 0, xfrm, w[2])
            # inside range
            else:
                f += buildStep(expterm * w[0],
                               lmax, 0, w[1], w[2])
    return f
