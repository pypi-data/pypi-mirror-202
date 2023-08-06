import math
from warnings import simplefilter
from itertools import zip_longest
from numpy import convolve, matrix, array
from numpy.linalg import LinAlgError
from numpy.linalg import matrix_power
from numpy.polynomial.polynomial import polypow
from scipy.special import binom
from scipy.linalg import fractional_matrix_power, expm, logm, sqrtm
from scipy.linalg._matfuncs_inv_ssq import LogmExactlySingularWarning

simplefilter('error', LogmExactlySingularWarning)

PRECISION = 32


def sqrt(x):
    if is_real(x):
        return HyperReal(sqrt(x))
    if isinstance(x, HyperReal):
        k = 0
        while not any(x[:2]):
            x <<= 2
            k += 1
        result = HyperReal.from_matrix(sqrtm(x.to_matrix(PRECISION))) >> k
        if 'nan' in str(result):
            raise ValueError
        return result


def sin(x):
    """calculates the sine of a hyperreal through the taylor series"""
    if isinstance(x, HyperReal) and x.st:
        _st, _inf = x.split()
        return math.sin(_st) * cos(_inf) + math.cos(_st) * sin(_inf)
    return sum((-1 if n % 2 else 1) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1) for n in range(PRECISION))


def cos(x):
    """calculates the cosine of a hyperreal through the taylor series"""
    if isinstance(x, HyperReal) and x.st:
        _st, _inf = x.split()
        return math.cos(_st) * cos(_inf) - math.sin(_st) * sin(_inf)
    return sum((-1 if n % 2 else 1) * (x ** (2 * n)) / math.factorial(2 * n) for n in range(PRECISION))


def tan(x):
    return sin(x) / cos(x)


def superscript_int(n, enclose=False):
    if enclose:
        return f'⁽{superscript_int(n)}⁾'
    return ''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(digit)] for digit in str(n))


def matrix_to_matrix(M, N):
    """calculates a matrix to the power of another matrix through the exponential series"""
    return expm(logm(M) * N)


def hyperrealify(function):
    """decorator to parse all real number arguments into hyperreals"""

    def inner(*args):
        return function(*(HyperReal(arg) if is_real(arg) else arg for arg in args))

    return inner


def is_real(x):
    return isinstance(x, bool) or isinstance(x, int) or isinstance(x, float)


def exp(x):
    if is_real(x):
        return HyperReal(math.exp(x))
    if isinstance(x, HyperReal):
        return HyperReal.from_matrix(expm(x.to_matrix(PRECISION)))


def log(x, base=None):
    if base:
        return log(x) / log(base)
    if is_real(x):
        return HyperReal(math.log(x))
    if isinstance(x, HyperReal):
        return HyperReal.from_matrix(logm(x.to_matrix(PRECISION)))


def repr_polynomial(coefficients, variable, mode):
    """makes a nice looking representation of polynomial. useful for polynomials of infinitesimals"""

    def enclose(text, condition):
        return f'({text})' if condition else text

    p = ['unicode', 'pythonic'].index(mode)
    s = ''
    c = 0
    for i, v in enumerate(coefficients):
        if not v:
            continue
        s += ('-' if v < 0 else '+') if c else ''
        s += (str(abs(v)) if i == 0 or v != 1 else '') + ('*' if v != 1 and i > 0 and p else '')
        s += enclose(variable + ((superscript_int(i) if not p else f'**{i}') if i > 1 else ''), p and i > 1) if i else ''
        c += 1
    return enclose(s, c > 1) if c else '0'


class HyperReal(tuple):
    def __new__(cls, *args):
        if not args:
            return tuple.__new__(cls, (0,))
        if not all(is_real(arg) for arg in args):
            raise ValueError('arguments must be real')
        return tuple.__new__(cls, args)

    def __repr__(self):
        return repr_polynomial(self, 'ε', 'pythonic')

    def __str__(self):
        return repr_polynomial(self, 'ε', 'unicode')

    @hyperrealify
    def __eq__(self, other):
        return all(x == y for x, y in zip_longest(self, other, fillvalue=0))

    @hyperrealify
    def __lt__(self, other):
        for x, y in zip_longest(self, other, fillvalue=0):
            if x < y:
                return True
            elif x > y:
                return False
        return False

    @hyperrealify
    def __le__(self, other):
        return (self < other) or (self == other)

    @hyperrealify
    def __gt__(self, other):
        return not (self <= 0)

    @hyperrealify
    def __ge__(self, other):
        return not (self < other)

    def __neg__(self):
        return HyperReal(*(-x for x in self))

    @hyperrealify
    def __sub__(self, other):
        return self.__add__(-other)

    @hyperrealify
    def __rsub__(self, other):
        return -self.__sub__(other)

    @hyperrealify
    def __add__(self, other):
        return HyperReal(*(x + y for x, y in zip_longest(self, other, fillvalue=0)))

    @hyperrealify
    def __rand__(self, other):
        """Returns the dot product (element-wise multiplication)"""
        return other.__and__(self)

    @hyperrealify
    def __and__(self, other):
        """Returns the dot product (element-wise multiplication)"""
        return HyperReal(*(x * y for x, y in zip_longest(self, other, fillvalue=0)))

    @hyperrealify
    def __radd__(self, other):
        return other.__add__(self)

    @hyperrealify
    def __mul__(self, other):
        return HyperReal(*convolve(self, other).tolist())

    @hyperrealify
    def __rmul__(self, other):
        return other.__mul__(self)

    def __truediv__(self, other):
        try:
            if is_real(other):
                return HyperReal(*(x / other for x in self))
            if isinstance(other, HyperReal):
                _self, _other = self, other
                while _other.inf and not _self.st and not _other.st:
                    _self <<= 1
                    _other <<= 1
                return _self * (_other ** -1)
        except ZeroDivisionError:
            raise ZeroDivisionError(f'division by infinitesimal')

    @hyperrealify
    def __rtruediv__(self, other):
        return other.__truediv__(self)

    def __floor__(self):
        _st, _inf = self.split()
        return math.floor(_st) - int(_st % 1 == 0 and _inf < 0)

    def __ceil__(self):
        _st, _inf = self.split()
        return math.ceil(_st) + int(_st % 1 == 0 and _inf > 0)

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

    @hyperrealify
    def __rpow__(self, other):
        return other.__pow__(self)

    def __pow__(self, power, modulo=None):
        if modulo:
            return self.__pow__(power) % modulo
        if isinstance(power, int) and power >= 0:
            return HyperReal(*polypow(self, power))
        try:
            if isinstance(power, int):
                return HyperReal.from_matrix(matrix_power(self.to_matrix(PRECISION), power))
            if isinstance(power, float):
                return HyperReal.from_matrix(fractional_matrix_power(self.to_matrix(PRECISION), power))
            if isinstance(power, HyperReal):
                return HyperReal.from_matrix(
                    matrix_to_matrix(self.to_matrix(PRECISION), power.to_matrix(PRECISION)))
        except LinAlgError:
            raise ZeroDivisionError(f'{self} cannot be raised to a negative power')
        except LogmExactlySingularWarning:
            raise ZeroDivisionError(f'{self} cannot be raised to an infinitesimal power')

    def __bool__(self):
        return any(self)

    def __round__(self, n=0):
        last_digit = round(self.st * (10 ** (n + 1))) % 10
        first_digits = math.floor(self.st * (10 ** n)) + int(last_digit == 5 and self.inf > 0)
        return round(first_digits * (10 ** - n), n)

    @staticmethod
    def from_matrix(M):
        """inverse of to_matrix"""
        return HyperReal(*(x for x in array(M[0, :]).flatten()))

    def to_matrix(self, terms=None):
        """converts hyperreal to an equivalently-behaving real matrix of dimension `terms`"""
        if terms is None:
            terms = len(self)
        return matrix([[self[x - y] if 0 <= x - y < len(self) else 0 for x in range(terms)] for y in range(terms)])

    @property
    def st(self):
        return self[0]

    @property
    def real(self):
        return self.st

    @property
    def inf(self):
        return HyperReal(0, *self[1:])

    def split(self):
        """splits hyperreal into standard and infinitesimal part"""
        return self.st, self.inf

    def __float__(self):
        return float(self.st)

    def __int__(self):
        return int(self.st)

    def __lshift__(self, other):
        """division by (ε ** other). truncates infinite part"""
        return HyperReal(*self[other:])

    def __rshift__(self, other):
        """multiplication by (ε ** other)"""
        return HyperReal(*([0] * other), *self)

    def is_integer(self):
        return self.st.is_integer()

    def is_real(self):
        return not self.inf


st = float


def inf(x):
    return x - float(x)


epsilon = ε = HyperReal(0, 1)


def auto_derivative(f, x, n=1):
    return sum((-1 if k % 2 else 1) * binom(n, k) * f(x + (n - k) * ε) for k in range(n))[n]


def limit(f, x):
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
    """decorator to fill in point-discontinuities using the `limit` method"""

    def inner(x):
        return limit(function, x)

    return inner
