from sympy import symbols
a, b, c, x = symbols("Fa Fb Fc x", real=True)

## Write your input data below

show = "F,V,M"
want=[(-1*x,(0,1)),(c,0,-1),(a,1,-1),(b,1,-2)]
lmax = 1
boundary_condition = [("V", lmax, 0),("M", 2/3, 0), ("M", lmax, 0)]

## above
