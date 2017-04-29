from sympy import symbols, simplify, integrate, solve
from PlotPrint import plotPrint
from StepFunc import StepFunc
from StepOperation import buildStep, weightMul
import UserInput


def rawtoStep(rawlist, lmax):
    x = symbols("x", real=True)
    f = 0
    for rawtuple in rawlist:
        if len(rawtuple) == 3:
            f += rawtuple[0] * StepFunc(x - rawtuple[1], rawtuple[2])
        elif len(rawtuple) == 2:
            # add to want
            poly, bound = simplify(rawtuple[0]), rawtuple[1]
            base = 0
            f += buildStep(poly, lmax, bound[0], bound[0], bound[1])
        else:
            raise ValueError
    return f


def recurGet(var):
    this = config[var]
    if this['data'] != None:
        return this['data']
    this['data'] = this['formula']()
    return this['data']


# input
show = UserInput.show.split(',')
weight = getattr(UserInput, 'weight', [])
want = UserInput.want
lmax = getattr(UserInput, 'lmax', 1)
boundary_condition = getattr(UserInput, 'boundary_condition', [])

# extract needed data
usevar = show + [d[0] for d in boundary_condition]
usevar = list(set(usevar))
raw_step = rawtoStep(want, lmax)

# output handle
c1, c2, x = symbols("c1 c2 x", real=True)
config = {
    'F': {'title': "Force",
          'data': raw_step,
          'arg': {'local': False, 'showplot': False}},
    'V': {'title': "Shear", 'arg': {},
          'formula': lambda: -integrate(recurGet('F'), x),
          'data': None},
    'M': {'title': "Moment", 'arg': {},
          'formula': lambda: -integrate(recurGet('V'), x),
          'data': None},
    'dy': {'title': "Angle", 'arg': {},
           'formula': lambda: -integrate(recurGet('M'), x) + c1,
           'data': None},
    'y': {'title': "Deflection", 'arg': {},
          'formula': lambda: -integrate(recurGet('dy'), x) + c2,
          'data': None},
    'T': {'title': "Torque",
          'data': raw_step,
          'arg': {'local': False, 'showplot': False}},

    'Fint': {'title': "Internal Force", 'arg': {},
             'formula': lambda: -integrate(recurGet('F'), x),
             'data': None},
    'P': {'title': "Pressure", 'arg': {},
          'formula': lambda: weightMul(recurGet('Fint'), weight, lmax),
          'data': None},
    'dx': {'title': "X-displacement", 'arg': {},
           'formula': lambda: integrate(recurGet('P'), x),
           'data': None},

    'Tint': {'title': "Internal Torque", 'arg': {},
             'formula': lambda: -integrate(recurGet('T'), x),
             'data': None},
    'A': {'title': "Twist Angle", 'arg': {},
          'formula': lambda: integrate(weightMul(
              recurGet('Tint'), weight, lmax), x),
          'data': None},
}

# Go Integrate
for s in usevar:
    recurGet(s)

# bc
if boundary_condition:
    bc = []
    usesymbols = set()
    for b in boundary_condition:
        bc.append(config[b[0]]['data'].subs({x: b[1]}) - b[2])
        usesymbols.update(bc[-1].free_symbols)
    ans = solve(bc, usesymbols)
    print(ans)
    for i in usevar:
        config[i]['data'] = config[i]['data'].subs(ans)

# output
for i in show:
    data = config[i]
    plotPrint(data['data'], lmax, data['title'], **data['arg'])
    print('-' * 16)
