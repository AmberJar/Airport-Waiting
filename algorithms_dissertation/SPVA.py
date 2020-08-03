import math
import datetime


starttime = datetime.datetime.now()

def SPVA(a, s, k, c):

    T = 18  # in hours

    # time unit
    t1 = 1 / s

    # number of times
    t = math.floor(T / t1)

    # create matrix for the data
    Matrix = [[0 for x in range(c + 1)] for y in range(t)]

    # loop for time period
    for n in range(0, t):

        # loop for length of queuing
        for j in range(0, c + 1):

            # define variable
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
            elif n > 0 and j < c:
                # initial value
                p1 = 0
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

            elif n > 0 and j == c:
                k1 = 0
                k2 = 0

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

                    # estimate of the probability that at least c new planes
                    for m in range(0, c - i + 1):
                        k2 = k2 + join(a, s, t1, n, m, k)

                    k2 = 1 - k2

                    p2 = p2 + Matrix[n - 1][i] * k2

                P = p1 + p2

                Matrix[n][j] = P

    AWT = []

    for i in range(0, t):

        mean_ql = 0
        awt = 0
        if i % 40 != 0:
            continue

        for j in range(0,c + 1):

            mean_ql = mean_ql + Matrix[i][j] * j

        awt = ((mean_ql + 0.5) * 1.5) * 40/60

        AWT.append(awt)

    return AWT


def binco(k, j):
    q = math.factorial(k - 1 + j)/(math.factorial(j) * math.factorial(k - 1))

    return q

def join(a, s, t1, n, j, k):
    q = binco(k, j) * (a[math.floor((n - 1) * t1)] ** j) * (k * s) ** k / (a[math.floor((n - 1) * t1)] + k * s) ** (k + j)
    return q



#based on funtion before
#calculate the total waiting time in each hour

#paramters definition
a = [35, 31, 28, 40, 33, 35, 37, 35, 38, 32, 32, 35, 31, 34, 28, 21, 28, 24]
s = 40
c = 50

#different values of k
k_changes = []

for k in range(1, 2):

    mean_time = []

    mean_time = SPVA(a, s, k, c)

    total_delay = 0

    for i in range(18):
        total_delay = total_delay + mean_time[i] * a[i]

    k_changes.append(total_delay)



print(k_changes)

endtime = datetime.datetime.now()

print(endtime - starttime)