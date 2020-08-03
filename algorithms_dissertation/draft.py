import math
import datetime
import random
import csv
import numpy as np

starttime = datetime.datetime.now()

T = 12  # in hours

def SPVA(a, s, k, c, Q):

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
            q = 0

            # start
            if n == 0 and j == Q:
                P = 1
                Matrix[n][j] = P


            # only the start, no planes
            elif n == 0 and j != Q:
                P = 0
                Matrix[n][j] = P

            # probability when the queues not reaching maximum
            elif n >= 1 and j < c:
                # initial value
                p2 = 0

                # estimate of the probability of j new planes joining the queue
                q = join(a, s, t1, n, j, k)

                # calculate the first part of the formula
                p1 = Matrix[n - 1][0] * q

                # calculate the second part of the Probability formula
                for i in range(1, j + 2):
                    p2 = p2 + Matrix[n - 1][i] * join(a, s, t1, n, j - i + 1, k)

                P = p1 + p2
                Matrix[n][j] = P

            elif n >= 1 and j == c:

                P = 1 - sum(Matrix[n][:])

                Matrix[n][j] = P



    AWT = []
    q_length = []

    for n in range(0, t):

        mean_ql = 0
        awt = 0

        for j in range(0, c + 1):

            mean_ql = mean_ql + Matrix[n][j] * j

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


def binco(k, j):
    q = math.factorial(k - 1 + j)/(math.factorial(j) * math.factorial(k - 1))

    return q


def join(a, s, t1, n, j, k):
    q = ((a[math.floor((n - 1) * t1)] ** j) * ((k * s) ** k)) / (a[math.floor((n - 1) * t1)] + k * s) ** (k + j)
    p = binco(k, j)
    tmp = p * q
    return tmp



#based on funtion before
#calculate the total waiting time in each hour

def total_waiting(a, s, k, c, Q):

    mean_time = SPVA(a, s, k, c, Q)

    total_delay = []
    for i in range(T):
        hour_delay = mean_time[i] * a[i]
        total_delay.append(hour_delay)

    #return total delay of each 18 hour (A 1 x 18 list)
    return total_delay

#paramters definition
a = [36, 37, 39, 38, 37, 37, 38, 40, 38, 33, 16, 1]
s = 40
c = 30
k = 10

for Q in range(31):

    A = total_waiting(a, s, k, c, Q)
    print(sum(A))


endtime = datetime.datetime.now()

print(endtime - starttime)






