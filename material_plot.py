from sympy import symbols, simplify, integrate, \
    linsolve, degree, LC, LT, expand
from StepFunc import StepFunc
from PlotPrint import plotPrint


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


plotPrint(f, lmax, "Force", local=False, showplot=False)
plotPrint(v, lmax, "Shear")
plotPrint(m, lmax, "Moment")
