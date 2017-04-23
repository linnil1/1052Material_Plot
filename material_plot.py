from sympy import symbols, simplify, integrate, solve
from PlotPrint import plotPrint
from StepFunc import StepFunc
from StepOperation import buildStep, weightMul


def rawtoStep(rawlist, lmax):
    f = 0
    for rawtuple in rawlist:
        if len(rawtuple) == 3:
            f += rawtuple[0] * StepFunc(rawtuple[1], rawtuple[2])
        elif len(rawtuple) == 2:
            # add to want
            poly, bound = simplify(rawtuple[0]), rawtuple[1]
            base = 0
            f += buildStep(poly, lmax, bound[0], bound[0], bound[1])
        else:
            raise ValueError
    return f


x = symbols("x", real=True)
show = "f,v,m,y,dy,p,dx"
weight = []

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
boundary_condition = []

# three boundary
want=[(-1*x,(x-0,x-1)),(c,x-0,-1),(a,x-1,-1),(b,x-1,-2)]
lmax = 1
boundary_condition = [("v", lmax, 0),("m", 2/3, 0), ("m", lmax, 0)]

# deflection
show = "f,y,dy"
want=[(a,x-0,-1),(-1,x-1/2,-1),(b,x-1,-1)]
lmax = 1
boundary_condition = [("v", lmax, 0),("m", lmax, 0),("y",0,0),("y",lmax,0)]

# deflect with poly
show = "f,y,dy"
want=[(a,x-0,-1),(-1,(x-0,x-1)),(1,(x-1,x-2)),(-1,(x-2,x-3)),(b,x-3,-1)]
lmax = 3
boundary_condition = [("v", lmax, 0),("m", lmax, 0),("y",0,0),("y",lmax,0)]

# presure weight
show = "f,v,p"
want=[(a,x-0,-1),(-50,(x-0.4,x-0.6)),(b,x-1,-1)]
weight=[(2,0,0.2),(-2,0.8,1)]
lmax = 1
boundary_condition = [("v", lmax, 0), ("m", lmax, 0)]

# bounded beam with tension
show = "f,v,dx"
want=[(a,x-0,-1),(-10,x-0.3,-1),(b,x-1,-1)]
weight=[(0.2*1,0,0.3),(0.8*1,0.3,1)]
lmax = 1
boundary_condition = [("v", lmax, 0), ("dx", lmax, 0)]

# default
a, b, c = symbols("Fa Fb Fc", real=True)
show = "f,v,m,y,dy,p,dx"
"""

# input
a, b, c = symbols("Fa Fb Fc", real=True)
show = "f,v,dx"
want = [(a, x - 0, -1), (-10, x - 0.3, -1), (b, x - 1, -1)]
weight = [(0.2 * 1, 0, 0.3), (0.8 * 1, 0.3, 1)]
lmax = 1
boundary_condition = [("v", lmax, 0), ("dx", lmax, 0)]

# main calc
f = rawtoStep(want, lmax)
v = -integrate(f, x)
m = -integrate(v, x)
c1, c2 = symbols("c1 c2", real=True)
dy = integrate(m, x) + c1
y = integrate(dy, x) + c2
p = weightMul(v, weight, lmax)
dx = integrate(p, x)

# input handle
show = show.split(',')
use = show + [d[0] for d in boundary_condition]
use = list(set(use))

# output handle
config = {
    'f': {'title': "Force",
          'data': f,
          'arg': {'local': False, 'showplot': False}},
    'v': {'title': "Shear", 'arg': {},
          'data': v},
    'p': {'title': "Pressure", 'arg': {},
          'data': p},
    'm': {'title': "Moment", 'arg': {},
          'data': m},
    'y': {'title': "Deflection", 'arg': {},
          'data': y},
    'dx': {'title': "X-displacement", 'arg': {},
           'data': dx},
    'dy': {'title': "Angle", 'arg': {},
           'data': dy}}


# bc
if boundary_condition:
    bc = []
    usesymbols = set()
    for b in boundary_condition:
        bc.append(config[b[0]]['data'].subs({x: b[1]}) - b[2])
        usesymbols.update(bc[-1].free_symbols)
    ans = solve(bc, usesymbols)
    print(ans)
    for i in use:
        config[i]['data'] = config[i]['data'].subs(ans)

# output
for i in show:
    data = config[i]
    plotPrint(data['data'], lmax, data['title'], **data['arg'])
