import unittest
import numpy
import material_plot
from sympy import symbols, Rational, simplify, integrate
from StepFunc import StepFunc

class TestStep(unittest.TestCase):
    def setUp(self):
        self.x = symbols("x", real=True)

    def test_def(self):
        x = self.x
        s = 4 * StepFunc(x - 1, 3)
        for i in numpy.arange(1, 2, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), 4 * (i - 1) ** 3, 2)
        self.assertEqual(s.subs({x:0}), 0)
        self.assertEqual(s.subs({x:1}), 0)

    def test_step(self):
        x = self.x
        lmax = 2

        # F
        s = StepFunc(x - 1, 0)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), 1, 2)
        self.assertEqual(s.subs({x:0}), 0)

        # V
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), i - 1, 2)
        self.assertEqual(s.subs({x:0}), 0)

        # M
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), (i - 1)**2 / 2, 2)
        self.assertEqual(s.subs({x:0}), 0)

    def test_step_special(self):
        x = self.x
        lmax = 2

        # F
        s = StepFunc(x - 1, -2)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), 0, 2)
        self.assertEqual(s.subs({x:0}), 0)
        self.assertEqual(s.subs({x:1}), 0)

        # V
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), 0, 2)
        self.assertEqual(s.subs({x:0}), 0)
        self.assertEqual(s.subs({x:1}), 0)

        # M
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), -1, 2)
        self.assertEqual(s.subs({x:0}), 0)
        self.assertEqual(s.subs({x:1}), -1)

    def test_step_coeff(self):
        x = self.x
        lmax = 1

        # F
        s = -4 * StepFunc(x - Rational(1, 2), 1)
        # V
        s = integrate(s, x)
        for i in numpy.arange(0, lmax, 0.1):
            if i < 0.5:
                self.assertAlmostEqual(s.subs({x:i}), 0, 2)
            else:
                self.assertAlmostEqual(s.subs({x:i}), -2 * (i - 0.5) ** 2, 2)
        self.assertAlmostEqual(s.subs({x:1}), -0.5, 2)

    def test_step_multi(self):
        x = self.x
        lmax = 3

        # F
        s = StepFunc(x - 1, -1) + 2 * StepFunc(x - 2, 0)
        for i in numpy.arange(1, lmax, 0.1):
            if i < 2:
                self.assertAlmostEqual(s.subs({x:i}), 0, 2)
            else:
                self.assertAlmostEqual(s.subs({x:i}), 2 * 1, 2)
        self.assertEqual(s.subs({x:0}), 0)
        self.assertEqual(s.subs({x:1}), 0)
        self.assertEqual(s.subs({x:2}), 2)
        self.assertEqual(s.subs({x:3}), 2)

        # V
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            if i < 2:
                self.assertAlmostEqual(s.subs({x:i}), 1, 2)
            else:
                self.assertAlmostEqual(s.subs({x:i}), 1 + 2 * (i - 2), 2)
        self.assertEqual(s.subs({x:0}), 0)
        self.assertEqual(s.subs({x:1}), 1)
        self.assertEqual(s.subs({x:2}), 1)
        self.assertEqual(s.subs({x:3}), 3)

        # M
        s = integrate(s, x)
        for i in numpy.arange(1, lmax, 0.1):
            if i < 2:
                self.assertAlmostEqual(s.subs({x:i}), i - 1, 2)
            else:
                self.assertAlmostEqual(s.subs({x:i}), i - 1 + (i - 2) ** 2, 2)
        self.assertEqual(s.subs({x:0}), 0)
        self.assertEqual(s.subs({x:1}), 0)
        self.assertEqual(s.subs({x:2}), 1)
        self.assertEqual(s.subs({x:3}), 3)

    def test_equal(self):
        x = self.x
        s = StepFunc(x, 1) + StepFunc(x - 1, 0)
        ts = StepFunc(x, 1) - StepFunc(x - 1, 0) + 2 * StepFunc(x - 1, 0)
        for i in numpy.arange(0, 2, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), ts.subs({x:i}), 2)


class TestTransferToStep(unittest.TestCase):
    def setUp(self):
        self.x = symbols("x", real=True)
        self.lmax = 1

    def test_step(self):
        x = self.x
        want = [(3,0,1)]
        ms = material_plot.rawtoStep(want, self.lmax)
        s = 3 * StepFunc(x - 0, 1)

        for i in numpy.arange(0, self.lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), ms.subs({x:i}), 2)

    def test_step_range(self):
        x = self.x
        want = [(3,(1,2))]
        self.lmax = 3
        ms = material_plot.rawtoStep(want, self.lmax)
        s = 3 * StepFunc(x - 1, 0) - 3 * StepFunc(x - 2, 0)
        for i in numpy.arange(0, self.lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), ms.subs({x:i}), 2)

    def test_step_range_x(self):
        x = self.x
        want = [(2 * x + 4,(1,2))]
        self.lmax = 3
        ms = material_plot.rawtoStep(want, self.lmax)
        s = 4 * StepFunc(x - 1, 0) + 2 * StepFunc(x - 1, 1) \
          - 6 * StepFunc(x - 2, 0) - 2 * StepFunc(x - 2, 1)
        for i in numpy.arange(0, self.lmax, 0.1):
            self.assertAlmostEqual(s.subs({x:i}), ms.subs({x:i}), 2)
        self.assertEqual(s.subs({x:4}), 0)


if __name__ == '__main__':
    unittest.main()
