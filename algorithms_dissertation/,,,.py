import math

def binco(k, j):
    q = math.factorial(k - 1 + j)/(math.factorial(j) * math.factorial(k - 1))

    return q


def join(a, s, t1, n, j, k):
    q = ((a[math.floor((n - 1) * t1)] ** j) * ((k * s) ** k)) / (a[math.floor((n - 1) * t1)] + k * s) ** (k + j)
    p = binco(k, j)
    tmp = p * q
    return tmp

a = [36, 37, 39, 38, 37, 37, 38, 40, 38, 33, 16, 1]
s = 2
c = 5
k = 10