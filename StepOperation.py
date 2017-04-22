from StepFunc import StepFunc
from sympy import degree, LC, symbols, Add, Mul


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
                xfrm = - m.args[0] + x
                expterm = term.expand(lim=lmax, func=True)
                func = m

        for w in wei:
            # outside range
            if w[2] <= xfrm:
                continue
            # partical inside range
            elif w[1] <= xfrm <= w[2]:
                f += buildStep(expterm * w[0],
                               lmax, x, x - xfrm, x - w[2])
            # inside range
            else:
                f += buildStep(expterm * w[0],
                               lmax, x, x - w[1], x - w[2])
    return f
