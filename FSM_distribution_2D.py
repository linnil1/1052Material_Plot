from sympy import symbols, simplify, Function, integrate
from sympy import solve, linsolve
from sympy import degree, LC, LT, expand, LM
from sympy.plotting import plot

class StepFunc(Function):
    nargs = 2

    @classmethod
    def eval(cls, x, n):
        x = simplify(x)
        if len(x.free_symbols):
            return None
        if x < 0:
            return 0
        elif n < 0 :
            return 0
        return x**n

    def _eval_Integral(self,a="x"):
        if self.args[1] == -1:
            return StepFunc(self.args[0],self.args[1]+1)
        return StepFunc(self.args[0],self.args[1]+1)/(self.args[1]+1)

    def _eval_expand_func(self, **hints):
        x,n = self.args
        if n < 0 :
            return 0
        if x.subs({symbols('x'):hints['lim']}) < 0:
            return 0
        return x**n

def sectionSeparate(formula):
    a = set([ x-LM(f).args[0] for f in formula.args if len(f.atoms(StepFunc))])
    a.update([0,lmax])
    a = list(sorted(a))
    st = 0
    formularr = []
    for c in a[1:]:
        print(formula.expand(lim=st,func=True))
        formularr.append( (formula.expand(lim=st,func=True), (x,st,c)) )
        st = c
    return formularr

def localpoint(farr):
    localmm = set()
    print("LOCAL MIN_MAX")
    for formula in farr:
        #first
        formula = (formula[0],formula[1])
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

def FtoStep(l):
    f = 0
    for i in l:
        if len(i)==3:
            f += i[0]*StepFunc(i[1],i[2])
        elif len(i)==2:
            # add to want
            poly, pos = i[0], i[1]
            base = 0
            while poly != 0 :
                add = LC(poly,x)* StepFunc(pos[0], degree(poly,x))
                base += add.subs({x:lmax})
                f += add
                poly = poly - LT(poly,x)

            # add to zero
            while base != 0 : #how about <0
                cut = -LC(base,x)* StepFunc(pos[1], degree(base,x))
                f += cut
                base = base + cut.subs({x:lmax})
        else:
            raise ValueError
    return f

def main(f):
    v =  -integrate(f,x)
    m =  -integrate(v,x)
    return v,m

a,b,x = symbols("a b x")
lmax = 10
needsolve = False #True
#want = [(5,x-0,-1),(-50,(x-0.4,x-0.6)),(5,x-1,-1)]
#want = [(a,x-0,-1),(-50,(x-0.3,x-0.5)),(b,x-1,-1)]
#want = [(5,x-0,-1),(-1000*x,(x-0.4,x-0.5)),(-100+1000*x,(x-0.5,x-0.6)),(5,x-1,-1)]
#want = [ (2,x-0,-1), (1,x-1/3,-2), (1,x-2/3,-2), (-2,x-1,-1) ]
#want = [ (-0.8,(x-3,x-7)), (a,x-4,-1), (b,x-6,-1), (-2,x-3,-1),(-2,x-7,-1) ]
want = [ (1,x-0,-1), (-0.8,(x-3,x-7)), (3.6,x-4,-1), (3.6,x-6,-1), (-3,x-2,-1),(-3,x-8,-1), (1,x-10,-1) ]
#want = [ (-1,(x-0,x-0.5)), (a,x-0,-1), (b,x-0,-2) ]
#want = [ (-1*x,(x-0,x-2/3)), (a,x-0,-1), (b,x-2/3,-1) ]
#want = [ (-1*x,(x-0,x-1)), (0.074074074,x-0,-1), (a,x-1,-1),(b,x-1,-2) ]

f = FtoStep(want)
v,m = main(f)
if needsolve:
    ans = linsolve([v.subs({x:lmax}), m.subs({x:lmax})], (a,b)) .args[0]
    ans = [(a,ans[0]),(b,ans[1])]
    print(ans)
    f = f.subs(ans)
    v,m = main(f)

print("FORCE")
print(f)
print("Shear")
print(v)
arr = sectionSeparate(v)
localpoint(arr)
plot(*arr)
print("Moment")
print(m)
arr = sectionSeparate(m)
localpoint(arr)
plot(*arr)
