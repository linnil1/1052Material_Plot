from sympy import Function, Basic, simplify, symbols, init_printing
from sympy.printing.str import StrPrinter


class StepFunc(Function):
    nargs = 2

    @classmethod
    def eval(cls, x, n):
        x = simplify(x)
        if len(x.free_symbols):
            return None
        if x < 0:
            return 0
        elif n < 0:
            return 0
        return x**n

    def _eval_Integral(self, a="x"):
        x, n = self.args
        if n == -1:
            return StepFunc(x, n + 1)
        return StepFunc(x, n + 1) / (n + 1)

    def _eval_expand_func(self, **hints):
        x, n = self.args
        if n < 0:
            return 0
        if x.subs({symbols('x', real=True): hints['lim']}) < 0:
            return 0
        return x**n

#    def _hashable_content(self): #hack
#        x = symbols('x')
#        return ( x-self.args[0], self.args[1] )

    def sort_key(self, order=None):  # hack
        # https://github.com/sympy/sympy/blob/master/sympy/core/compatibility.py
        return ((4, 0, 'StepFunc'),
                (1, ((-self.args[0]).sort_key(),)),
                self.args[1].sort_key(),
                1)

    def _sympystr(self, printer):
        return "<{}>{} ".format(self.args[0], self.args[1])

    def _latex(self, printer):
        return r"\left \langle {} \right \rangle _ {{{}}}".format(
            self.args[0], self.args[1])


init_printing()

"""
class StepFuncPrinter(StrPrinter):
    def _print_StepFunc(self, expr):
        return "<{}>{} ".format(expr.args[0], expr.args[1])

Basic.__str__ = lambda self: StepFuncPrinter().doprint(self)
"""
