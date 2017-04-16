from sympy import symbols, simplify, integrate, \
    solve, degree, LC, LT, expand, init_printing
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
            # how about <0
            cut = -LC(base, x) * StepFunc(bound[1], degree(base, x))
            while base != 0:
                base += cut.expand(lim=lmax, func=True)
                f += cut
        else:
            raise ValueError
    return f


x = symbols("x", real=True)
show = "f,v,m,y,dy"

"""
# test if it is same
want=[(5,x-0,-1),(-50,(x-0.4,x-0.6)),(5,x-1,-1)]
want=[(a,x-0,-1),(-50,(x-0.4,x-0.6)),(b,x-1,-1)]
lmax = 1
boundary_condition = [("v", lmax, 0), ("m", lmax, 0)]

# use ploy x
want=[(5,x-0,-1),(-1000*x,(x-0.4,x-0.5)),(-100+1000*x,(x-0.5,x-0.6)),(5,x-1,-1)]
lmax = 1
boundary_condition = [("v", lmax, 0), ("m", lmax, 0)]

# solve moment
want=[(2,x-0,-1),(1,x-1/3,-2),(1,x-2/3,-2),(-2,x-1,-1)]
want=[(-1,(x-0,x-1)),(a,x-0,-1),(b,x-0,-2)]
lmax = 1
boundary_condition = [("v", lmax, 0), ("m", lmax, 0)]

# lmax=10
want=[(1,x-0,-1),(-0.8,(x-3,x-7)),(3.6,x-4,-1),(3.6,x-6,-1),(-3,x-2,-1),(-3,x-8,-1),(1,x-10,-1)]
boundary_condition = [("v", lmax, 0), ("m", lmax, 0)]

# three boundary
want=[(-1*x,(x-0,x-1)),(c,x-0,-1),(a,x-1,-1),(b,x-1,-2)]
lmax = 1
boundary_condition = [("v", lmax, 0),("m", 2/3, 0), ("m", lmax, 0)]

# deflection
show = "f,y,dy"
want=[(a,x-0,-1),(-1,x-1/2,-1),(b,x-1,-1)]
lmax = 1
boundary_condition = [("v", lmax, 0),("m", lmax, 0),("y",0,0),("y",lmax,0)]

# default
a, b, c = symbols("Fa Fb Fc", real=True)
latex = True
show = "f,y,dy"
want=[(a,x-0,-1),(-1,x-1/2,-1),(b,x-1,-1)]
lmax = 1
boundary_condition = [("v", lmax, 0),("m", lmax, 0),("y",0,0),("y",lmax,0)]
"""

# input

# cal
f = rawtoStep(want)
v = -integrate(f, x)
m = -integrate(v, x)
c1, c2 = symbols("c1 c2", real=True)
dy = integrate(m, x) + c1
y = integrate(dy, x) + c2

# bc
if boundary_condition:
    bc = []
    usesymbols = set()
    for b in boundary_condition:
        bc.append(eval(b[0]).subs({x: b[1]}) - b[2])
        usesymbols.update(bc[-1].free_symbols)
    ans = solve(bc, usesymbols)
    print(ans)
    f = f.subs(ans)
    v = v.subs(ans)
    m = m.subs(ans)
    dy = dy.subs(ans)
    y = y.subs(ans)


# output
show = show.split(',')
if 'f' in show:
    plotPrint(f, lmax, "Force", tex=latex, local=False, showplot=False)
if 'v' in show:
    plotPrint(v, lmax, "Shear", tex=latex)
if 'm' in show:
    plotPrint(m, lmax, "Moment", tex=latex)
if 'y' in show:
    plotPrint(y, lmax, "Deflection", tex=latex)
if 'dy' in show:
    plotPrint(dy, lmax, "Angle", tex=latex)

# %matplotlib inline
# from IPython.display import Math
