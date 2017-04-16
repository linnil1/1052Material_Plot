from sympy import symbols, solve, LM, plot, latex
from StepFunc import StepFunc
from IPython.display import display, Math


def sectionSeparate(formula, lmax):
    x = symbols('x', real=True)
    pos = set([x - LM(f).args[0]
               for f in formula.args if len(f.atoms(StepFunc))])
    pos.update([0, lmax])
    pos = list(sorted(pos))
    st = 0
    formularr = []
    for en in pos[1:]:
        print(formula.expand(lim=st, func=True))
        formularr.append((formula.expand(lim=st, func=True), (x, st, en)))
        st = en
    return formularr


def localminmaxFind(formularr):
    localmm = set()
    x = symbols('x', real=True)
    print("LOCAL MIN_MAX")
    for formula in formularr:
        expr = formula[0]
        bound = formula[1][1], formula[1][2]

        # first diff and second diff
        x_possible = solve(expr.diff(x), x) + \
            solve(expr.diff(x).diff(x), x)
        x_valid = [x for x in x_possible if bound[0] <= x <= bound[1]]

        # bound position
        if bound[0] not in x_valid:
            x_valid.append(bound[0])
        if bound[1] not in x_valid:
            x_valid.append(bound[1])

        # update
        localmm.update([(xi, expr.subs({x: xi})) for xi in x_valid])

    for x, y in sorted(localmm):
        print("{} => {}".format(x, y))


def plotPrint(expr, lmax, title="", tex=False, show=True, local=True,
              showplot=True):
    if show:
        print(title)
        if tex:
            display(Math(latex(expr)))
        else:
            print(expr)
    arr = sectionSeparate(expr, lmax)
    if local and show:
        localminmaxFind(arr)
    if showplot:
        plot(*arr, title=title)
