import itertools as it
import more_itertools as mit
import numpy as np
import math
from scipy.special import binom


PRECISION = 32


def convolution_power(a, n):
    """De Pril, N. (1985). Recursions for Convolutions of Arithmetic Distributions"""
    b = [a[0] ** n]
    for k in range(1, len(a)):
        b.append(sum((((n + 1) * j - k) * a[j] * b[k - j]) / k for j in range(1, k + 1) if a[j] and b[k - j]) / a[0])
    return b


def superscript(n):
    """converts numbers to superscript strings. useful for exponents."""
    _superscript = {
        '-': '⁻',
        '.': '⋅',
        '0': '⁰',
        '1': '¹',
        '2': '²',
        '3': '³',
        '4': '⁴',
        '5': '⁵',
        '6': '⁶',
        '7': '⁷',
        '8': '⁸',
        '9': '⁹',
    }
    return ''.join(_superscript[character] for character in str(n))


def hyperrealify(function):
    """decorator to automatically convert arguments into type HyperReal"""
    def inner(*args):
        return function(*(HyperReal(arg) if isinstance(arg, int) or isinstance(arg, float) else arg for arg in args))
    return inner


def sqrt(x):
    return x ** .5


def log(x, base=None):
    """calculates the logarithm based on a series expansion from https://en.wikipedia.org/wiki/Natural_logarithm"""
    if base:
        return log(x) / log(base)
    _x = ((x - 1) / (x + 1))
    _x2 = _x * _x
    return 2 * _x * sum((_x2 ** n) / (2 * n + 1) for n in range(PRECISION))


def exp(x):
    """calculates the exponential function from its series expansion"""
    return 1 + x + sum((x ** n) / math.factorial(n) for n in range(2, PRECISION))


def sin(x):
    """calculates the sine through the taylor series"""
    return sum((-1 if n % 2 else 1) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1) for n in range(PRECISION))


def cos(x):
    """calculates the cosine through the taylor series"""
    return sum((-1 if n % 2 else 1) * (x ** (2 * n)) / math.factorial(2 * n) for n in range(PRECISION))


def tan(x):
    return sin(x) / cos(x)


class HyperReal:
    """A number class capable of representing infinitesimals and infinities"""
    def __init__(self, *coefficients, max_power=0):
        coefficients = list(coefficients)
        while any(coefficients) and not coefficients[0]:
            del coefficients[0]
            max_power -= 1
        self.coefficients = np.array(list(mit.padded(coefficients[:PRECISION], 0, PRECISION)), dtype=np.float64)
        self._max_power = max_power

    @property
    def max_power(self):
        return int(self._max_power) if int(self._max_power) == self._max_power else self._max_power

    def __repr__(self):
        if not self:
            return '0'

        def _str(x):
            s = str(x)
            if 'e' in s:
                i = s.index('e')
                s = s[:i] + '·10' + superscript(s[i+1:])
            return s

        string = ''
        terms = 0
        for i, coefficient in enumerate(self.coefficients):
            if not coefficient:
                continue
            power = i - self.max_power
            if int(power) == power:
                power = int(power)
            sign = '-' if coefficient < 0 else '+' if terms else ''
            mag = _str(abs(coefficient)) if power == 0 or abs(coefficient) != 1 else ''
            variable = 'ε' if power > 0 else 'ω' if power else ''
            power = superscript(abs(power)) if 0 != abs(power) != 1 else ''
            string += sign + mag + variable + power
            terms += 1
        return string if terms == 1 else '(%s)' % string

    def __getitem__(self, power):
        """returns the corresponding term with the same omega-power"""
        index = self.max_power - power
        if 0 <= index < len(self.coefficients):
            if int(index) == index:
                index = int(index)
            return self.coefficients[index]
        return 0

    @hyperrealify
    def __eq__(self, other):
        if not other:
            return not self
        if self.max_power != other.max_power:
            return False
        for x, y in it.zip_longest(self.coefficients, other.coefficients, fillvalue=0):
            if x != y:
                return False
        return True

    @hyperrealify
    def __lt__(self, other):
        if not other:
            return self[self.max_power] < 0
        if self.max_power < other.max_power:
            return True
        if self.max_power > other.max_power:
            return False
        for x, y in it.zip_longest(self.coefficients, other.coefficients, fillvalue=0):
            if x < y:
                return True
            elif x > y:
                return False
        return False

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __abs__(self):
        return -self if self < 0 else self

    @hyperrealify
    def __neg__(self):
        return HyperReal(*(-x for x in self.coefficients), max_power=self.max_power)

    @hyperrealify
    def __add__(self, other):
        max_power_dif = other.max_power - self.max_power
        if max_power_dif % 1:
            raise ValueError('cannot add power series with non-integer power differences')
        max_power_dif = int(max_power_dif)
        return HyperReal(*(a + b
                           for a, b in it.zip_longest(it.chain(it.repeat(0, max_power_dif), self.coefficients),
                                                      it.chain(it.repeat(0, -max_power_dif), other.coefficients),
                                                      fillvalue=0)),
                         max_power=max(self.max_power, other.max_power))

    @hyperrealify
    def __radd__(self, other):
        return other.__add__(self)

    @hyperrealify
    def __sub__(self, other):
        return self.__add__(-other)

    @hyperrealify
    def __rsub__(self, other):
        return other.__sub__(self)

    @hyperrealify
    def __mul__(self, other):
        return HyperReal(*np.convolve(self.coefficients, other.coefficients),
                         max_power=self.max_power + other.max_power)

    @hyperrealify
    def __rmul__(self, other):
        return other.__mul__(self)

    @hyperrealify
    def __truediv__(self, other):
        return self * (other ** -1)

    @hyperrealify
    def __rtruediv__(self, other):
        return other.__truediv__(self)

    @hyperrealify
    def __pow__(self, power, modulo=None):
        if modulo:
            return self.__pow__(power) % modulo
        if power == 0:
            return HyperReal(1)
        if is_real(power):
            power = power.real
            return HyperReal(*convolution_power(list(mit.padded(self.coefficients, 0, PRECISION)), power),
                             max_power=self.max_power * power)
        return (self ** st(power)) * exp(inf(power) * log(self))

    @hyperrealify
    def __rpow__(self, other):
        return other.__pow__(self)

    def __floor__(self):
        if self.max_power % 1:
            raise ValueError('non-integer infinite or infinitesimal powers cannot be floored')
        _sum = 0
        for power in range(0, self.max_power + 1):
            large_part = self[power]
            small_part = HyperReal(*self.coefficients[self.max_power + 1 - power:], max_power=power - 1)
            _sum += math.floor(large_part) * (omega ** power) - int(large_part % 1 == 0 and small_part < 0)
        return _sum

    def __ceil__(self):
        if self.max_power % 1:
            raise ValueError('non-integer infinite or infinitesimal powers cannot be ceiled')
        _sum = 0
        for power in range(0, self.max_power + 1):
            large_part = self[power]
            small_part = HyperReal(*self.coefficients[self.max_power + 1 - power:], max_power=power - 1)
            _sum += math.ceil(large_part) * (omega ** power) + int(large_part % 1 == 0 and small_part > 0)
        return _sum

    def __mod__(self, other):
        return self - other * (self // other)

    @hyperrealify
    def __rmod__(self, other):
        return other.__mod__(self)

    @hyperrealify
    def __floordiv__(self, other):
        return (self / other).__floor__()

    @hyperrealify
    def __rfloordiv__(self, other):
        return other.__floordiv__(self)

    def __round__(self, n=0):
        if self.max_power % 1:
            raise ValueError('non-integer infinite or infinitesimal powers cannot be rounded')
        _sum = 0
        for power in range(0, self.max_power + 1):
            large_part = self[power]
            small_part = HyperReal(*self.coefficients[self.max_power + 1 - power:], max_power=power - 1)
            last_digit = round(large_part * (10 ** (n + 1))) % 10
            first_digits = math.floor(large_part * (10 ** n)) + int(last_digit > 5 or (last_digit == 5 and small_part > 0))
            _sum += round(first_digits * (10 ** - n), n) * (omega ** power)
        return _sum

    def __int__(self):
        if not self - self[0]:
            return self[0]
        raise ValueError(f'cannot convert {self} to integer')

    def __bool__(self):
        return any(self.coefficients)

    @property
    def st(self):
        return self[0]

    @property
    def inf(self):
        return self - self.st

    @property
    def real(self):
        return self.st.real


epsilon = ε = HyperReal(1, max_power=-1)
omega = ω = HyperReal(1, max_power=1)


def is_real(x):
    return x.real == x


def st(x):
    return x.st if isinstance(x, HyperReal) else x


def inf(x):
    return x - st(x)


def limit(f, x):
    """calculates the limit of f(a) as a approaches x using the standard part"""
    if st(x) == x:
        left_limit, right_limit = limit(f, x - ε), limit(f, x + ε)
        if left_limit != right_limit:
            raise ValueError('left-hand and right-hand limits don\'t match')
        return right_limit
    try:
        return st(f(x))
    except Exception as e:
        raise ValueError(f'{e}\nlimit does not exist')


def continuous(function):
    """decorator to fill-in point-discontinuities using the `limit` method"""

    def inner(x):
        return limit(function, x)

    return inner


def auto_derivative(f, x, n=1):
    """automatically calculates the n'th derivative of f(x) via f'(x)=st((f(x+ε)-f(x))/ε)"""
    _sum = 0
    for k in range(1, n + 1):
        _f = f(x + k * ε)
        if n > 0 and not isinstance(_f, HyperReal):
            continue
        _sum += (-1 if (k + n) % 2 else 1) * binom(n, k) * _f[-n]
    return _sum
