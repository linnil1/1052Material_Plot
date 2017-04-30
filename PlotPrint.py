from sympy import symbols, solve, LM, plot, latex, N
from StepFunc import StepFunc
from IPython.display import display, Markdown


def sectionSeparate(formula, lmax):
    x = symbols('x', real=True)
    pos = set([x - LM(f).args[0]
               for f in formula.args if len(f.atoms(StepFunc))])
    pos.update([0, lmax])
    pos = list(sorted(pos))
    st = 0
    formularr = []
    # print("Line Segment Function")
    for en in pos[1:]:
        # print(formula.expand(lim=st, func=True))
        formularr.append((formula.expand(lim=st, func=True), (x, st, en)))
        st = en
    return formularr


def localminmaxFind(formularr):
    localmm = set()
    x = symbols('x', real=True)
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
        for xi in x_valid:
            nx = N(xi, 3)
            ny = N(round(expr.subs({x: xi}), 5), 3)
            localmm.update([(nx, ny)])

    return sorted(localmm)


def plotPrint(expr, lmax, title="", show=True, local=True,
              showplot=True):
    if show:
        if run_from_ipython():
            display(Markdown("# "+title))
            display(expr)
        else:
            print(title)
            print(expr)
    arr = sectionSeparate(expr, lmax)
    if showplot:
        # print(arr)
        p = plot(*arr, title=title, show=False)
        p = p.backend(p)
        if local and show:
            localmm = localminmaxFind(arr)
            for lmm in localmm:
                p.plt.text(*lmm, str(lmm))
            # how to deal with overlap
            # why adjustText no work
        p.show()


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
