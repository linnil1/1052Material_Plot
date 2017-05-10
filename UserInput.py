from material_plot import main
from sympy import symbols, Rational
a, b, c, x = symbols("Fa Fb Fc x", real=True)

## Write your input data below

r = Rational(1, 2)
show = "F,y,dy"
want=[(a,0,-1),(-1,(0,1)),(1,(1,2)),(-1,(2,3)),(b,3,-1)]
lmax = 3
boundary_condition = [("V", lmax, 0),("M", lmax, 0),("y",0,0),("y",lmax,0)]

## above

main(show, lmax, want, boundary_condition, weight=[])
