from sympy import symbols
a, b, c = symbols("Fa Fb Fc", real=True)

## Write your input data below

show = "F,y,dy"
want=[(a,0,-1),(-1,(0,1)),(1,(1,2)),(-1,(2,3)),(b,3,-1)]
lmax = 3
boundary_condition = [("V", lmax, 0),("M", lmax, 0),("y",0,0),("y",lmax,0)]

## above
