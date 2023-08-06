"""
包含常用常量与各种工具类
"""
import math
import random as rd

PI = math.pi
E = math.e

ALPHABET_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"

def num(a, b):
    a = int(a)
    b = int(b)
    if a < b:
        return rd.randint(a, b)
    else:
        return rd.randint(b, a)