from materialdiagram import main
from sympy import symbols, Rational
a, b, c, x = symbols("Fa Fb Fc x", real=True)

## Write your input data below

r = Rational(1, 2)
show = "F,y,dy"
external=[(a,0,-1),(-1,(0,1)),(1,(1,2)),(-1,(2,3)),(b,3,-1)]
length = 3
boundary = [("V", length, 0),("M", length, 0),("y",0,0),("y",length,0)]

## above

result = main(show, length, external, boundary, weight=[])
