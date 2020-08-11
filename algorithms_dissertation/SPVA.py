import math
import datetime
import random
import csv
import numpy as np

starttime = datetime.datetime.now()

T = 20  # in hours

def SPVA(a, s, k, c):

    global T

    P = 0

    # time unit
    t1 = 1 / s

    # number of times
    t = math.floor(T / t1)

    # create matrix for the data
    Matrix = [[0 for x in range(c +1)] for y in range(t)]

    # loop for time period
    for n in range(0, t):

        # loop for length of queuing
        for j in range(0, c + 1):

            # define variable
            P = 0
            q = 0

            # start
            if n == 0 and j == 0:
                P = 1
                Matrix[n][j] = P

            # only the start, no planes
            elif n == 0 and j != 0:
                P = 0
                Matrix[n][j] = P

            # probability when the queues not reaching maximum
            elif n >= 1 and j < c:
                # initial value
                p1 = 0
                p2 = 0
                q = 0

                # estimate of the probability of j new planes joining the queue
                q = join(a, s, t1, n, j, k)

                # calculate the first part of the formula
                p1 = Matrix[n - 1][0] * q

                # calculate the second part of the Probability formula
                for i in range(1, j + 2):
                    p2 = p2 + Matrix[n - 1][i] * join(a, s, t1, n, (j - i + 1), k)

                P = p1 + p2
                Matrix[n][j] = P

            elif n >= 1 and j == c:

                k1 = 0

                # initial value
                p1 = 0
                p2 = 0

                # calculate the first part of the formula
                for m in range(0, c):
                    k1 = k1 + join(a, s, t1, n, m, k)

                k1 = 1 - k1

                p1 = Matrix[n - 1][0] * k1

                # calculate the second part of the Probability formula
                for i in range(1, c + 1):

                    par = c - i + 1

                    k2 = 0

                    # estimate of the probability that at least c new planes
                    for m in range(0, par):

                        k2 = k2 + join(a, s, t1, n, m, k)

                    k2 = 1 - k2

                    p2 = p2 + Matrix[n - 1][i] * k2

                P = p1 + p2

                Matrix[n][j] = P



    q_length = []

    for n in range(0, t):

        mean_ql = 0
        awt = 0

        for j in range(0, c + 1):

            mean_ql = mean_ql + Matrix[n][j] * j

            if n == 8 * c:
                print(Matrix[n][j])



        q_length.append(mean_ql)

    results = [] #AWT hourly

    for i in range(0, T):

        hour_q = 0

        for j in range(s):

            hour_q = hour_q + q_length[s * i + j]

        hour_awt = (hour_q/40 + 0.5) * 1.5
        results.append(hour_awt)

    #return the results of average delay in different hours
    return results

def join(a, s, t1, n, j, k):

    q1 = k * s
    q2 = a[math.floor(t1 * (n - 1))]

    q = ((q1**k) * (q2**j))/((q1 + q2)**(k + j))

    p = math.factorial(k - 1 + j)/(math.factorial(j) * math.factorial(k - 1))

    tmp = p * q
    return tmp

#paramters definition
a = [6, 12, 36, 39, 35, 43, 42, 35, 36, 36, 33, 32, 32, 32, 32, 31, 31, 31, 31, 33]
s = 40
c = 30
k = 9
#different values of k
k_changes = []

def total_waiting(a, s, k, c):

    mean_time = SPVA(a, s, k, c)

    total_delay = []
    for i in range(T):
        total_delay.append(mean_time[i] * a[i])

    #return total delay of each 18 hour (A 1 x 18 list)
    return total_delay


A = sum(total_waiting(a, s, k, c))
print(A)

endtime = datetime.datetime.now()

print(endtime - starttime)