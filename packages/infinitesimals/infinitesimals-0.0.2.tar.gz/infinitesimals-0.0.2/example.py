from __init__ import *
import __init__ as infintesimals
from math import floor, ceil
from sys import float_info

"""Example program for demonstrating the capabilities of the infinitesimal library"""


def main():

    print('initializing hyperreals is easy')
    x = HyperReal(1, 2, 1)  # also try "x = 1.0 + 2.0 * ε + (ε ** 2)" or "1.0 + 2.0 * epsilon + (epsilon ** 2)"
    print(x == (1.0 + 2.0 * ε + (ε ** 2)) == (1.0 + 2.0 * epsilon + (epsilon ** 2)), '\n')

    print('ε really is an infinitesimal, and not just a really small number')
    smallest_float = float_info.min  # 2.2250738585072014e-308
    print(0 < ε < smallest_float)
    largest_float = float_info.max  # 1.7976931348623157e+308
    print((ε ** 2) * largest_float < ε * smallest_float, '\n')

    print('hypereals have many built-in capabilities')
    print(dir(HyperReal), '\n')

    print('every hyperreal, x, has a standard part st(x)==x.st, and infinitesimal part inf(x)==x.inf')
    print(f'{x=}, st(x)={x.st}, inf(x)={x.inf}', '\n')

    print('pythonic alternative for displaying hyperreals')
    print(repr(x), '\n')

    print('you can set how many terms will be used in calculations\n')
    infintesimals.PRECISION = 10

    print('they support all elementary operations')
    print(f'1 / x = {1 / x}')
    print(f'x % 1 = {x % 1}')
    print(f'2 ** x = {2 ** x}\n')

    print('and common elementary operations')
    print(f'exp(x) = {exp(x)}')
    print(f'log(x) = {log(x)}')
    print(f'sin(x) = {sin(x)}\n')

    infintesimals.PRECISION = 32  # default precision

    print('their rounding behaviour is also consistent')
    print(f'floor(1 - ε) = {floor(1 - ε)}')
    print(f'ceil(10 + ε) = {ceil(10 + ε)}')
    print(f'round(0.5 + ε) = {round(0.5 + ε)}')
    print(f'round(0.5 - ε) = {round(0.5 - ε)}\n')

    print('but most excitingly, they work as an efficient alternative to symbolic or numeric analysis')
    print('for example, limits involving point discontinuities become trivial')

    def f(x):
        return (2 ** x - 3 ** x) / x

    print(f'st(f(ε)) = {st(f(ε))}\n')

    print('which is employed in the `limit` method')

    def g(x):
        return x * x / (1 - cos(x))

    print(f'limit of g(x) as x -> 0 = {limit(g, 0)}\n')

    print(f'and is further used in the `continuous` decorator')

    @continuous
    def sinc(x):
        return sin(x) / x

    print(f'sinc(0) = {sinc(0)}\n')

    print('automatic derivation is also made easy')

    def h(x):
        return x ** x

    def h_prime(x):
        return st((f(x + ε) - f(x)) / ε)

    print(f'h\'(1) = {h_prime(x)}\n')
    print('which is conveniently used in the `auto_derivative` method')
    print(f'h{superscript_int(10, enclose=True)}(1) = {auto_derivative(h, 1, 10)}\n')

    try:
        print(f'1 / ε = {1 / ε}')
    except ZeroDivisionError as e:
        print(f'ZeroDivisionError: {e}')
        print('at the moment, infinities are not supported, but plan on being in a future version\n')

    print('hope you enjoy the infinitesimals library!')
    print('try commenting out various pieces code to play around with different features and limitations')

if __name__ == '__main__':
    main()