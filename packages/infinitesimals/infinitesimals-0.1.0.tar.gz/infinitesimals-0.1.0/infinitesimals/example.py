import __init__ as infinitesimals
from __init__ import *
from math import floor, ceil
from sys import float_info

"""Example program for demonstrating the capabilities of the infinitesimal library"""


def main():
    print('Initializing hyperreals is easy.')
    x = 1 + 2 * ε + (ε ** 2)  # also try "x = 1.0 + 2.0 * epsilon + (epsilon ** 2)"
    print(f'x = {x}', '\n')

    print('ε really is an infinitesimal, and not just a really small number!')
    smallest_float = float_info.min  # 2.2250738585072014e-308
    print(0 < ε < smallest_float)
    largest_float = float_info.max  # 1.7976931348623157e+308
    print((ε ** 2) * largest_float < ε * smallest_float, '\n')

    print('HyperReals have many built-in capabilities.')
    print(dir(HyperReal), '\n')

    print('Every HyperReal, x, has a standard part st(x)==x.st, and infinite(simal) part inf(x)==x.inf.')
    print(f'x = {x}, st(x) = {x.st}, inf(x) = {x.inf}.', '\n')

    print('You can set how many terms will be used in calculations.\n')
    infinitesimals.PRECISION = 10

    print('They support all arithmetical operations:')
    print(f'1 / x = {1 / x},')
    print(f'x % 1 = {x % 1},')
    print(f'2 ** x = {2 ** x},\n')

    print('and common elementary functions:')
    print(f'exp(x) = {exp(x)},')
    print(f'log(x) = {log(x)},')
    print(f'sin(x) = {sin(x)}.\n')

    infinitesimals.PRECISION = 32  # default precision

    print('Their rounding behaviour is also consistent.')
    print(f'floor(1 - ε) = {floor(1 - ε)},')
    print(f'ceil(10 + ε) = {ceil(10 + ε)},')
    print(f'round(0.5 + ε) = {round(0.5 + ε)},')
    print(f'round(0.5 - ε) = {round(0.5 - ε)}.\n')

    print('But perhaps most excitingly, they work as an efficient alternative to symbolic or numeric analysis.')
    print('For example, limits involving point discontinuities become trivial.')

    def f(x):
        return (2 ** x - 3 ** x) / x

    print(f'limit of f(x) as x -> 0+ = {st(f(ε))}.\n')

    print('Which is employed in the `limit` method:')

    def g(x):
        return x * x / (1 - cos(x))

    print(f'limit of g(x) as x -> 0 = {limit(g, 0)}.\n')

    print(f'The `limit` method is further used in the `continuous` decorator:')

    @continuous
    def sinc(x):
        return sin(x) / x

    print(f'sinc(0) = {sinc(0)}.\n')

    print('Automatic derivation is also made easy:')

    def h(x):
        return x ** x

    def h_prime(x):
        return st((h(x + ε) - h(x)) / ε)

    print(f'h\'(1) = {h_prime(1)},\n')
    print('which is conveniently used in the `auto_derivative` method:')
    print(f'10th derivative of h at x=1 is {auto_derivative(h, 1, 10)}.\n')

    print('Note: Errors are likely due to too low PRECISION or floating-point errors.')
    print('However, any float-like-class which behave like floats should be compatible coefficients for HyperReals.\n')

    print('The inverse of an infinitesimal is an infinity,')
    print(f'1 / ε = {1 / ε}.\n')

    print('Again, ω really is an infinity, and not just a really big number.')
    print(0 < ε < smallest_float < 1 < largest_float < ω, '\n')

    print('You can perform arithmetic with infinities just like you would infinitesimals.\n')

    print('But again, perhaps most interestingly, is its convenience in non-standard analysis:')
    print(f'limit of sinc(x) as x -> ∞ = {limit(sinc, ω)}.\n')

    print('Hope you enjoy the infinitesimals library!')
    print('Try commenting out various pieces code to play around with different features and limitations.\n')


if __name__ == '__main__':
    main()