import math
from numpy.lib.arraysetops import ediff1d
import scipy
from sympy import *


class GBM_constants:
    a = 0  # 8 # 100
    b = 0  # 0.1 # 12
    n = 0  # 10

    Es = 0
    Ed = 0
    Rs = 0
    Rd = 0

    def __init__(self, rs, rd, n):
        self.n = n
        self.Rs = rs
        self.Rd = rd

        self.a = self.AB(self.Rs)
        self.b = self.AB(self.Rd)
        self.Es = self.ES()
        self.Ed = self.ED()

    def g(self):
        y = Symbol('y', real=True)
        f = y + (2 * self.a - y)**(1/2) + (2 * self.b - y)**(1/2)
        fprime = f.diff(y)

        rez = solve(fprime, y)
        if rez[0] < 0:
            max_y = 0
        elif rez[0] > 2*self.b:
            max_y = 2*self.b
        else:
            max_y = rez[0]

        return max_y + math.sqrt(2 * self.a - max_y) + math.sqrt(2 * self.b - max_y)

    def check(self, left):
        right = 2 * self.b + math.sqrt(6 * self.b)
        if (left >= right):
            return True
        else:
            return False

    def ED(self):
        return (2 * self.b + math.sqrt(6 * self.b)) * (math.log(self.n, 2) / self.n)

    def ES(self):
        fistPart = self.a/2 - math.sqrt(self.a)
        secondPart = self.a + self.b - self.g()
        left = fistPart if fistPart < secondPart else secondPart
        if (self.check(left) != True):
            print("WARNING: With this variables a, b, n accuracy is low!")
        return left * (math.log(self.n, 2)/self.n)

    def R(self, var):
        return var * math.log(self.n, 2) / self.n

    def AB(self, rs):
        return rs * self.n / math.log(self.n, 2)
