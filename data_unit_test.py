# testing code

import unittest
import numpy
from StepFunc import StepFunc
from sympy import symbols, Rational, simplify, integrate
from material_plot import boundarySolve, rawtoStep, goIntegrate
from StepOperation import weightMul


class TestStep(unittest.TestCase):
    def setUp(self):
        self.x = symbols("x", real=True)

    def test_def(self):
        x = self.x
        s = 4 * StepFunc(x - 1, 3)
        for i in numpy.arange(1, 2, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), 4 * (i - 1) ** 3, 2)
        self.assertEqual(s.subs({x: 0}), 0)
        self.assertEqual(s.subs({x: 1}), 0)

    def test_step(self):
        x = self.x
        lmax = 2

        # F
        s = StepFunc(x - 1, 0)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), 1, 2)
        self.assertEqual(s.subs({x: 0}), 0)

        # V
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), i - 1, 2)
        self.assertEqual(s.subs({x: 0}), 0)

        # M
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), (i - 1) ** 2 / 2, 2)
        self.assertEqual(s.subs({x: 0}), 0)

    def test_step_special(self):
        x = self.x
        lmax = 2

        # F
        s = StepFunc(x - 1, -2)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), 0, 2)
        self.assertEqual(s.subs({x: 0}), 0)
        self.assertEqual(s.subs({x: 1}), 0)

        # V
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), 0, 2)
        self.assertEqual(s.subs({x: 0}), 0)
        self.assertEqual(s.subs({x: 1}), 0)

        # M
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), -1, 2)
        self.assertEqual(s.subs({x: 0}), 0)
        self.assertEqual(s.subs({x: 1}), -1)

    def test_step_coeff(self):
        x = self.x
        lmax = 1

        # F
        s = -4 * StepFunc(x - Rational(1, 2), 1)
        # V
        s = integrate(s, x)
        for i in numpy.arange(0, lmax, 0.1):
            if i < 0.5:
                self.assertAlmostEqual(s.subs({x: i}), 0, 2)
            else:
                self.assertAlmostEqual(s.subs({x: i}), -2 * (i - 0.5) ** 2, 2)
        self.assertAlmostEqual(s.subs({x: 1}), -0.5, 2)

    def test_step_multi(self):
        x = self.x
        lmax = 3

        # F
        s = StepFunc(x - 1, -1) + 2 * StepFunc(x - 2, 0)
        for i in numpy.arange(1, lmax, 0.1):
            if i < 2:
                self.assertAlmostEqual(s.subs({x: i}), 0, 2)
            else:
                self.assertAlmostEqual(s.subs({x: i}), 2 * 1, 2)
        self.assertEqual(s.subs({x: 0}), 0)
        self.assertEqual(s.subs({x: 1}), 0)
        self.assertEqual(s.subs({x: 2}), 2)
        self.assertEqual(s.subs({x: 3}), 2)

        # V
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            if i < 2:
                self.assertAlmostEqual(s.subs({x: i}), 1, 2)
            else:
                self.assertAlmostEqual(s.subs({x: i}), 1 + 2 * (i - 2), 2)
        self.assertEqual(s.subs({x: 0}), 0)
        self.assertEqual(s.subs({x: 1}), 1)
        self.assertEqual(s.subs({x: 2}), 1)
        self.assertEqual(s.subs({x: 3}), 3)

        # M
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            if i < 2:
                self.assertAlmostEqual(s.subs({x: i}), i - 1, 2)
            else:
                self.assertAlmostEqual(s.subs({x: i}), i - 1 + (i - 2) ** 2, 2)
        self.assertEqual(s.subs({x: 0}), 0)
        self.assertEqual(s.subs({x: 1}), 0)
        self.assertEqual(s.subs({x: 2}), 1)
        self.assertEqual(s.subs({x: 3}), 3)

    def test_equal(self):
        x = self.x
        s = StepFunc(x, 1) + StepFunc(x - 1, 0)
        ts = StepFunc(x, 1) - StepFunc(x - 1, 0) + 2 * StepFunc(x - 1, 0)
        for i in numpy.arange(0, 2, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), ts.subs({x: i}), 2)


class TestTransferToStep(unittest.TestCase):
    def setUp(self):
        self.x = symbols("x", real=True)
        self.lmax = 1

    def test_step(self):
        x = self.x
        want = [(3, 0, 1)]
        ms = rawtoStep(want, self.lmax)
        s = 3 * StepFunc(x - 0, 1)

        for i in numpy.arange(0, self.lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), ms.subs({x: i}), 2)

    def test_step_range(self):
        x = self.x
        want = [(3, (1, 2))]
        self.lmax = 3
        ms = rawtoStep(want, self.lmax)
        s = 3 * StepFunc(x - 1, 0) - 3 * StepFunc(x - 2, 0)
        for i in numpy.arange(0, self.lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), ms.subs({x: i}), 2)
        self.assertEqual(s.subs({x: 4}), 0)

    def test_step_range_x(self):
        x = self.x
        want = [(2 * x + 4, (1, 2))]
        self.lmax = 3
        ms = rawtoStep(want, self.lmax)
        s = 4 * StepFunc(x - 1, 0) + 2 * StepFunc(x - 1, 1) \
            - 6 * StepFunc(x - 2, 0) - 2 * StepFunc(x - 2, 1)
        for i in numpy.arange(0, self.lmax, 0.1):
            self.assertAlmostEqual(s.subs({x: i}), ms.subs({x: i}), 2)

    def test_weight_ori(self):
        x = self.x
        self.lmax = 4
        s = rawtoStep([(x + 1, (1, self.lmax))], self.lmax)
        ts = weightMul(s, [], self.lmax)
        self.assertEqual(s - ts, 0)

    def test_weight_over(self):
        x = self.x
        self.lmax = 4
        s = rawtoStep([(x + 1, (1, self.lmax))], self.lmax)
        ts = weightMul(s, [[2, 0, 4]], self.lmax)
        self.assertEqual(s * 2 - ts, 0)

    def test_weight_inside(self):
        x = self.x
        self.lmax = 4
        s = rawtoStep([(x + 1, (1, self.lmax))], self.lmax)
        ts = weightMul(s, [[2, 1, 3]], self.lmax)
        for i in numpy.arange(0, self.lmax, 0.1):
            if 1 <= i < 3:
                self.assertAlmostEqual(ts.subs({x: i}), s.subs({x: i}) * 2, 2)
            else:
                self.assertAlmostEqual(ts.subs({x: i}), s.subs({x: i}), 2)
        self.assertEqual(ts.subs({x: 5}), 0)

    def test_weight_left(self):
        x = self.x
        self.lmax = 4
        s = rawtoStep([(x + 1, (1, self.lmax))], self.lmax)
        ts = weightMul(s, [[2, 0, 2]], self.lmax)
        for i in numpy.arange(0, self.lmax, 0.1):
            if 0 <= i < 2:
                self.assertAlmostEqual(ts.subs({x: i}), s.subs({x: i}) * 2, 2)
            else:
                self.assertAlmostEqual(ts.subs({x: i}), s.subs({x: i}), 2)
        self.assertEqual(ts.subs({x: 5}), 0)

    def test_weight_right(self):
        x = self.x
        self.lmax = 4
        s = rawtoStep([(x + 1, (1, self.lmax))], self.lmax)
        ts = weightMul(s, [[2, 2, 4]], self.lmax)
        for i in numpy.arange(0, self.lmax, 0.1):
            if 2 <= i < 4:
                self.assertAlmostEqual(ts.subs({x: i}), s.subs({x: i}) * 2, 2)
            else:
                self.assertAlmostEqual(ts.subs({x: i}), s.subs({x: i}), 2)
        self.assertEqual(ts.subs({x: 5}), 0)


class TestSolve(unittest.TestCase):
    def setUp(self):
        self.x = symbols("x", real=True)
        self.lmax = 1

    def test_step_M(self):
        x = self.x
        want = [(-1, 0, -1), (2, 1 / 2, -1), (-1, 1, -1)]
        usevar = ['M']
        config = goIntegrate(want, [], self.lmax, usevar)
        s = rawtoStep(want, self.lmax)
        self.assertEqual(config['F']['data'] - s, 0)
        s = integrate(s, x)
        self.assertEqual(config['V']['data'] + s, 0)
        s = integrate(s, x)
        self.assertEqual(config['M']['data'] - s, 0)

    def test_step_A(self):
        x = self.x
        want = [(-1, 0, -1), (2, 1 / 2, -1), (-1, 1, -1)]
        usevar = ['A']
        config = goIntegrate(want, [], self.lmax, usevar)
        s = rawtoStep(want, self.lmax)
        self.assertEqual(config['T']['data'] - s, 0)
        s = integrate(s, x)
        self.assertEqual(config['Tint']['data'] + s, 0)
        s = integrate(s, x)
        self.assertEqual(config['A']['data'] + s, 0)

    def test_step_dx(self):
        x = self.x
        want = [(-1, 0, -1), (2, 1 / 2, -1), (-1, 1, -1)]
        usevar = ['dx']
        config = goIntegrate(want, [], self.lmax, usevar)
        s = rawtoStep(want, self.lmax)
        self.assertEqual(config['F']['data'] - s, 0)
        s = integrate(s, x)
        self.assertEqual(config['Fint']['data'] + s, 0)
        self.assertEqual(config['P']['data'] + s, 0)
        s = integrate(s, x)
        self.assertEqual(config['dx']['data'] + s, 0)

    def test_solve_M(self):
        x = self.x
        a, b = symbols('a b')
        want = [(a, 0, -1), (2, Rational(1, 2), -1), (b, 1, -1)]
        usevar = ['F', 'V', 'M']
        config = goIntegrate(want, [], self.lmax, usevar)
        boundarySolve(config, [('V', self.lmax, 0),
                               ('M', self.lmax, 0)], usevar)

        # ans
        want = [(-1, 0, -1), (2, Rational(1, 2), -1), (-1, 1, -1)]
        s = rawtoStep(want, self.lmax)
        self.assertEqual(config['F']['data'] - s, 0)

    def test_solve_simple_support(self):
        x = self.x
        a, b = symbols('a b')
        want = [(a, 0, -1), (2, Rational(1, 2), -1), (b, 1, -1)]
        usevar = ['F', 'V', 'M', 'dy', 'y']
        config = goIntegrate(want, [], self.lmax, usevar)
        bound = [('V', self.lmax, 0), ('M', self.lmax, 0),
                 ('y', 0, 0), ('y', self.lmax, 0)]
        boundarySolve(config, bound, usevar)

        # ans: deflection formula of simple support beam
        for i in numpy.arange(0, 0.5, 0.01):
            self.assertAlmostEqual(config['y']['data'].subs({x: i}),
                                   (3 / 4 - i ** 2) * i / 6, 3)

    def test_solve_cantilever(self):
        x = self.x
        a, b = symbols('a b')
        want = [(a, 0, -1), (1, 1, -1), (b, 0, -2)]
        usevar = ['F', 'V', 'M', 'dy', 'y']
        config = goIntegrate(want, [], self.lmax, usevar)
        bound = [('V', self.lmax, 0), ('M', self.lmax, 0),
                 ('y', 0, 0), ('dy', 0, 0)]
        boundarySolve(config, bound, usevar)

        # ans: deflection formula of cantilever
        for i in numpy.arange(0, 1, 0.01):
            self.assertAlmostEqual(config['y']['data'].subs({x: i}),
                                   (3 - i) * i ** 2 / 6, 3)

    def test_solve_dx(self):
        # axis load with deformation in x
        x = self.x
        a, b = symbols('a b')
        want = [(a, 0, -1), (1, 0.3, -1), (b, 1, -1)]
        usevar = ['F', 'Fint', 'P', 'dx']
        # constrain on both ends
        # weight are different
        weight = [[7 / 10, 0, 0.3], [3 / 10, 0.3, 1]]
        config = goIntegrate(want, weight, self.lmax, usevar)
        bound = [('dx', self.lmax, 0), ('Fint', self.lmax, 0)]
        boundarySolve(config, bound, usevar)

        # ans
        want = [(-0.5, 0, -1), (1, 0.3, -1), (-0.5, 1, -1)]
        s = rawtoStep(want, self.lmax)
        for i in numpy.arange(0, 1, 0.1):
            self.assertAlmostEqual(
                config['F']['data'].subs({x: i}),  s.subs({x: i}), 2)

    def test_solve_A(self):
        # axis load with angle deformation
        x = self.x
        a, b = symbols('a b')
        want = [(a, 0, -1), (1, 0.3, -1), (b, 1, -1)]
        usevar = ['T', 'Tint', 'A']
        # constrain on both ends
        # weight are different
        weight = [[7 / 10, 0, 0.3], [3 / 10, 0.3, 1]]
        config = goIntegrate(want, weight, self.lmax, usevar)
        bound = [('A', self.lmax, 0), ('Tint', self.lmax, 0)]
        boundarySolve(config, bound, usevar)

        # ans
        want = [(-0.5, 0, -1), (1, 0.3, -1), (-0.5, 1, -1)]
        s = rawtoStep(want, self.lmax)
        for i in numpy.arange(0, 1, 0.1):
            self.assertAlmostEqual(
                config['T']['data'].subs({x: i}),  s.subs({x: i}), 2)


if __name__ == '__main__':
    unittest.main()
