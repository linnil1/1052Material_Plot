from sympy import symbols, solve, LM, plot
from StepFunc import StepFunc


def sectionSeparate(formula, lmax):
    x = symbols('x')
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
    x = symbols('x')
    print("LOCAL MIN_MAX")
    for formula in formularr:
        # first
        expr = formula[0]
        bound = formula[1][1], formula[1][2]
        fdiff = solve(expr.diff(x), x)
        fdiff = [fd for fd in fdiff if bound[0] < fd < bound[1]]
        localmm.update([(fd, expr.subs(x, fd)) for fd in fdiff])
        # second
        fdiff = solve(expr.diff(x).diff(x), x)
        fdiff = [fd for fd in fdiff if bound[0] < fd < bound[1]]
        localmm.update([(fd, expr.subs(x, fd)) for fd in fdiff])

        # endpoint
        if bound[0] not in fdiff:
            localmm.update(
                [(bound[0], expr.subs(x, bound[0]))])
        if bound[1] not in fdiff:
            localmm.update(
                [(bound[1], expr.subs(x, bound[1]))])

    for x, y in sorted(localmm):
        print("{} => {}".format(x, y))


def plotPrint(expr, lmax, title="", show=True, local=True, showplot=True):
    if show:
        print(title)
        print(expr)
    arr = sectionSeparate(expr, lmax)
    if local and show:
        localminmaxFind(arr)
    if showplot:
        plot(*arr, title=title)
