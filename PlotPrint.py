from sympy import symbols, solve, LM, plot, latex, N, Add, Mul, sign
from StepFunc import StepFunc
from IPython.display import display, Markdown


def sectionSeparate(formula, lmax):
    x = symbols('x', real=True)
    pos = set([x - LM(f).args[0]
               for f in Add.make_args(formula) if len(f.atoms(StepFunc))])
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


def sectionContinuous(formularr, ax):
    x_break = y_break = 0
    x = symbols('x', real=True)
    for formula in formularr:
        y_new = formula[0].subs({x: x_break})
        if y_break != y_new:
            ax.plot((x_break, x_break), (y_break, y_new), 'b-')
        x_break = formula[1][2]
        y_break = formula[0].subs({x: x_break})
    if y_break != 0:  # last one
        ax.plot((x_break, x_break), (y_break, 0), 'b-')


def impluseFind(expr):
    x = symbols('x', real=True)
    imparr = []
    for ex in Add.make_args(expr):
        mul = 1
        x_impulse = x_moment = None
        for f in Mul.make_args(ex):
            if isinstance(f, StepFunc):
                if f.args[1] == -1:
                    x_impulse = x - f.args[0]
                if f.args[1] == -2:
                    x_moment = x - f.args[0]
            else:
                mul *= f
            if x_impulse != None:
                imparr.append((x_impulse, mul, -1))
            elif x_moment != None:
                imparr.append((x_moment, mul, -2))

    return imparr


def impluseDraw(expr, ax):
    headwidth = 0.1
    imparr = impluseFind(expr)
    for imp in imparr:
        if imp:
            x, y = imp[0], imp[1]
            ax.arrow(x, 0, 0., float(y),
                     length_includes_head=True,
                     head_width=headwidth,  head_length=headwidth / 2)
            if imp[2] == -2:
                ax.arrow(x, 0, 0., float(y - sign(y) * headwidth / 2),
                         length_includes_head=True,
                         head_width=headwidth,  head_length=headwidth / 2)

            ax.text(x, y, str((N(x, 3), N(y, 3))))
            if y > ax.get_ylim()[1]:
                ax.set_ylim(top=float(y))
            if y < ax.get_ylim()[0]:
                ax.set_ylim(bottom=float(y))


def localminmaxDraw(arr, ax):
    localmm = localminmaxFind(arr)
    for lmm in localmm:
        ax.text(*lmm, str(lmm))
    # how to deal with overlap
    # why adjustText no work


def plotPrint(expr, lmax, title=""):
    # title expr
    if run_from_ipython():
        display(Markdown("# " + title))
        display(expr)
    else:
        print(title)
        print(expr)

    # main plot
    arr = sectionSeparate(expr, lmax)
    p = plot(*arr, title=title, show=False, line_color='b')
    p = p.backend(p)

    # some additional thing
    localminmaxDraw(arr, p.ax)
    sectionContinuous(arr, p.ax)
    impluseDraw(expr, p.ax)

    p.show()


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
