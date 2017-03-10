from sympy import symbols, expand, solve
from sympy import degree,LC,LT
from sympy.plotting import plot

class stepfunc: # This should improved 
    def __init__(self,w,st,n):
        self.w  = w
        self.st = st
        self.n  = n
    def __repr__(self):
        return "{}<{}>_{}".format(self.w,self.st,self.n)
    def __str__(self):
        return "{}<{}>_{}".format(self.w,self.st,self.n)

    def calc(self,m):
        if self.st.subs(x,m) < 0: 
            return 0
        return self.w*(self.st**self.n)

    def integrate(self):
        if self.n == -1:
            return stepfunc(self.w, self.st, self.n+1)
        return stepfunc(self.w/(self.n+1), self.st, self.n+1)

    def __mul__(self,num):
        return stepfunc(self.w*num, self.st, self.n)

def printlist(l):
    [print(i) for i in l]

x,l = symbols('x l')

def draw(l):
    a = set([x-i.st for i in l])
    a.update([0,1])
    a = list(sorted(a))
    st = 0
    formularr = []
    for c in a[1:]:
        formula = 0
        for i in l:
            formula += i.calc(st)
        #print( formula,(x,st,c) )
        #print( expand(formula) )
        formularr.append( (formula,(x,st,c) ) )
        st = c
    localpoint(formularr)
    plot(*formularr)
    return formularr

def localpoint(fl):
    localmm = set()
    print("LOCAL MIN_MAX")
    for formula in fl:
        #first
        fdiff =  solve(formula[0].diff(x),x)
        fdiff = [fd for fd in fdiff if formula[1][1] < fd < formula[1][2]]
        localmm.update( [ (fd,formula[0].subs(x,fd)) for fd in fdiff ] )
        #second
        fdiff =  solve(formula[0].diff(x).diff(x),x)
        fdiff = [fd for fd in fdiff if formula[1][1] < fd < formula[1][2]]
        localmm.update( [ (fd,formula[0].subs(x,fd)) for fd in fdiff ] )

        #endpoint
        if formula[1][1] not in fdiff:
            localmm.update([ (formula[1][1],formula[0].subs(x,formula[1][1])) ])
        if formula[1][2] not in fdiff:
            localmm.update([ (formula[1][2],formula[0].subs(x,formula[1][2])) ])

    for i in sorted(localmm):
        print( "{} => {}".format(i[0],i[1]) )

def shrink(l):
    if not l:
        return []
    l = sorted(l,key=lambda a:(x-a.st,a.n))
    newone = [l[0]]
    for i in l[1:]:
        if i.st == newone[-1].st and i.n == newone[-1].n:
            newone[-1].w += i.w
        else:
            newone.append(i)

    # zero weigth
    l = []
    for i in newone:
        if i.w!=0:
            l.append(i)
    return l 

def FtoStep(l):
    f = []
    for i in l:
        if len(i)==3:
            f.append( stepfunc(*i) )
        elif len(i)==2:
            # add to want
            poly, pos = i[0], i[1]
            base = 0
            while poly != 0 :
                add = stepfunc( LC(poly,x), pos[0], degree(poly,x))
                base += add.calc(1)
                f.append( add )
                poly = poly - LT(poly,x)

            # add to zero
            while base != 0 : #how about <0
                cut = stepfunc(-LC(base,x), pos[1], degree(base,x))
                f.append( cut )
                base = base + cut.calc(1)
        else:
            raise ValueError
    return shrink(f)

want = [(5,x-0,-1),(-50,(x-0.4,x-0.6)),(5,x-1,-1)]
#want = [(5,x-0,-1),(-1000*x,(x-0.4,x-0.5)),(-100+1000*x,(x-0.5,x-0.6)),(5,x-1,-1)]
#want = [ (2,x-0,-1), (1,x-1/3,-2), (1,x-2/3,-2), (-2,x-1,-1) ]
#want = [ (2,x-0,-1), (1,x-1/3,-2), (1,x-2/3,-2), (-2,x-1,-1) ]

print("FORCE")
f = FtoStep(want)
printlist(f)

print("Shear")
v = [ i.integrate()*-1 for i in f ]
printlist(v)
draw(v)

print("Moment")
m = [ i.integrate()*-1 for i in v ]
printlist(m)
fl = draw(m)

