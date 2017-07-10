#!/usr/bin/env python3
import math
d = {'michael':95, 'bob':75, 'tar':85}
a = 'abc'
print(a)
a = a.replace('a', 'A')
print(a)
b = {'ab':(3,[1,2,3])}
print(b['ab'])
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x, -x
    else:
        return -x, x
print(my_abs(-8))
def move(x, y, step, angle = 0):
    nx = x + step * math.cos(angle)
    return nx
print(move(100,100,60,math.pi/6))
def power(x, n=2):
    s = 1
    while n > 0:
        n -= 1
        s = s * x
    return s
print(power(3,3))