from sympy import symbols, simplify, Function, integrate, Basic, \
    solve, linsolve, degree, LC, LT, expand, LM, plot

from sympy.printing.str import StrPrinter


class StepFunc(Function):
    nargs = 2

    @classmethod
    def eval(cls, x, n):
        x = simplify(x)
        if len(x.free_symbols):
            return None
        if x < 0:
            return 0
        elif n < 0:
            return 0
        return x**n

    def _eval_Integral(self, a="x"):
        x, n = self.args
        if n == -1:
            return StepFunc(x, n + 1)
        return StepFunc(x, n + 1) / (n + 1)

    def _eval_expand_func(self, **hints):
        x, n = self.args
        if n < 0:
            return 0
        if x.subs({symbols('x'): hints['lim']}) < 0:
            return 0
        return x**n

#    def _hashable_content(self): #hack
#        x = symbols('x')
#        return ( x-self.args[0], self.args[1] )

    def sort_key(self, order=None):  # hack
        # https://github.com/sympy/sympy/blob/master/sympy/core/compatibility.py
        return ((4, 0, 'StepFunc'), (1, ((-self.args[0]).sort_key(),)), self.args[1].sort_key(), 1)


class StepFuncPrinter(StrPrinter):
    def _print_StepFunc(self, expr):
        return "<{}>{} ".format(expr.args[0], expr.args[1])


Basic.__str__ = lambda self: StepFuncPrinter().doprint(self)


def sectionSeparate(formula):
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


def localpoint(formularr):
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


def rawtoStep(rawlist):
    f = 0
    for rawtuple in rawlist:
        if len(rawtuple) == 3:
            f += rawtuple[0] * StepFunc(rawtuple[1], rawtuple[2])
        elif len(rawtuple) == 2:
            # add to want
            poly, bound = rawtuple[0], rawtuple[1]
            base = 0
            while poly != 0:
                add = LC(poly, x) * StepFunc(bound[0], degree(poly, x))
                base += add.expand(lim=lmax, func=True)
                f += add
                poly -= LT(poly, x)

            # add to zero
            while base != 0:  # how about <0
                cut = -LC(base, x) * StepFunc(bound[1], degree(base, x))
                base += cut.expand(lim=lmax, func=True)
                f += cut
        else:
            raise ValueError
    return f


def main(f):
    v = -integrate(f, x)
    m = -integrate(v, x)
    return v, m


a, b, x = symbols("a b x")
lmax = 10
needsolve = False  # True
# want=[(5,x-0,-1),(-50,(x-0.4,x-0.6)),(5,x-1,-1)]
# want=[(a,x-0,-1),(-50,(x-0.3,x-0.5)),(b,x-1,-1)]
# want=[(5,x-0,-1),(-1000*x,(x-0.4,x-0.5)),(-100+1000*x,(x-0.5,x-0.6)),(5,x-1,-1)]
# want=[(2,x-0,-1),(1,x-1/3,-2),(1,x-2/3,-2),(-2,x-1,-1)]
# want=[(-0.8,(x-3,x-7)),(a,x-4,-1),(b,x-6,-1),(-2,x-3,-1),(-2,x-7,-1)]
# want=[(1,x-0,-1),(-0.8,(x-3,x-7)),(3.6,x-4,-1),(3.6,x-6,-1),(-3,x-2,-1),(-3,x-8,-1),(1,x-10,-1)]
# want=[(-1,(x-0,x-0.5)),(a,x-0,-1),(b,x-0,-2)]
# want=[(-1*x,(x-0,x-2/3)),(a,x-0,-1),(b,x-2/3,-1)]
# want=[(-1*x,(x-0,x-1)),(0.074074074,x-0,-1),(a,x-1,-1),(b,x-1,-2)]

f = rawtoStep(want)
v, m = main(f)
if needsolve:
    ans = linsolve([v.subs({x: lmax}), m.subs({x: lmax})], (a, b)) .args[0]
    ans = [(a, ans[0]), (b, ans[1])]
    print(ans)
    f = f.subs(ans)
    v, m = main(f)


print("FORCE")
print(f)
print("Shear")
print(v)
arr = sectionSeparate(v)
localpoint(arr)
plot(*arr)
print("Moment")
print(m)
arr = sectionSeparate(m)
localpoint(arr)
plot(*arr)
