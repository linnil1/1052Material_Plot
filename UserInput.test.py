# test ans correct
show = "F,V,M"
want=[(5,0,-1),(-50,(0.4,0.6)),(5,1,-1)]
want=[(a,0,-1),(-50,(0.4,0.6)),(b,1,-1)]
lmax = 1
boundary_condition = [("V", lmax, 0), ("M", lmax, 0)]

# use ploy x
show = "F,V,M"
want=[(5,0,-1),(-1000*x,(0.4,0.5)),(-100+1000*x,(0.5,0.6)),(5,1,-1)]
lmax = 1
boundary_condition = [("V", lmax, 0), ("M", lmax, 0)]

# solve moment
show = "F,V,M"
want=[(2,0,-1),(1,1/3,-2),(1,2/3,-2),(-2,1,-1)]
want=[(-1,(0,1)),(a,0,-1),(b,0,-2)]
lmax = 1
boundary_condition = [("V", lmax, 0), ("M", lmax, 0)]

# lmax=10
show = "F,V,M"
want=[(1,0,-1),(-0.8,(3,7)),(3.6,4,-1),(3.6,6,-1),(-3,2,-1),(-3,8,-1),(1,10,-1)]
lmax = 10
boundary_condition = []

# three boundary
show = "F,V,M"
want=[(-1*x,(0,1)),(c,0,-1),(a,1,-1),(b,1,-2)]
lmax = 1
boundary_condition = [("V", lmax, 0),("M", 2/3, 0), ("M", lmax, 0)]

# deflection
show = "F,y,dy"
want=[(a,0,-1),(-1,(0,1)),(1,(1,2)),(-1,(2,3)),(b,3,-1)]
lmax = 3
boundary_condition = [("V", lmax, 0),("M", lmax, 0),("y",0,0),("y",lmax,0)]

# weight : a const times your stepfunc
show = "F,Fint,P"
want = [(a,0,-1),(-10,0.3,-1),(b,1,-1)]
weight = [(0.7*1,0,0.3),(0.3*1,0.3,1)]
lmax = 1
boundary_condition = [("V",lmax,0),("dx",lmax,0)]

# bounded beam with tension
show = "F,Fint,dx"
want = [(a,0,-1),(-10,0.3,-1),(b,1,-1)]
weight = [(0.7*1,0,0.3),(0.3*1,0.3,1)]
lmax = 1
boundary_condition = [("Fint",lmax,0),("dx",lmax,0)]

# bounded beam with Torque
show = "T,Tint,A"
want = [(a,0,-1),(-10,0.3,-1),(b,1,-1)]
weight = [(0.7*1,0,0.3),(0.3*1,0.3,1)]
lmax = 1
boundary_condition = [("Tint",lmax,0),("A",lmax,0)]
