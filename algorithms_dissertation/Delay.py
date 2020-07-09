import math
import csv

global T

T = 18  # in hours


def main(a, s, k, c):
    P = 0

    # time unit
    t1 = (k + 1) / (k * s)

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
                q = join(a, s, t1, n, j)

                # calculate the first part of the formula
                p1 = Matrix[n - 1][0] * q

                # calculate the second part of the Probability formula
                for i in range(1, j + 2):
                    p2 = p2 + Matrix[n - 1][i] * join(a, s, t1, n, j - i + 1)

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
                    k1 = k1 + join(a, s, t1, n, m)

                k1 = 1 - k1

                p1 = Matrix[n - 1][0] * k1

                # calculate the second part of the Probability formula
                for i in range(1, c + 1):

                    # estimate of the probability that at least c new planes
                    for m in range(0, c - i + 1):
                        k2 = k2 + join(a, s, t1, n, m)

                    k2 = 1 - k2

                    p2 = p2 + Matrix[n - 1][i] * k2

                P = p1 + p2

                Matrix[n][j] = P


    data = []
    q_length = []

    for i in range(0, t):

        mean_ql = 0
        aqt = 0

        for j in range(0,c + 1):

            mean_ql = mean_ql + Matrix[i][j] * j

        mean_ql = mean_ql * 4/3

        aqt = (mean_ql + 0.5) * 1.5

        q_length.append(mean_ql)
        data.append(aqt)

    print(q_length)
    print(data)

    hour_q_length = []

    for i in range(0, 18):

        hour_q = 0

        for j in range(30):
            hour_q = hour_q + q_length[30 * i + j]

        hour_q_length.append(hour_q * 2)

    print(hour_q_length)




    #for i in range(0, t):
     #   for j in range(0, c + 1):
      #      if i % (1 / t1) == 0:
       #          print(f"hour{round(i / 30, 2)} planes{j}  time T{i} probability", Matrix[i][j])
        #         data.append(Matrix[i][j])

    #with open("file.csv", 'w', newline='') as f:
      #  w = csv.writer(f)
       # w.writerow(data)

    #for i in range(18):
     #   for j in range(51 * i, 51 * ( i + 1)) :
      #      print(data[j], end = ",")
       # print(end="\n")



    return 0





def join(a, s, t1, n, j):
    q = (((a[math.floor((n - 1) * t1)] / s) ** j) *
         math.exp(-a[math.floor((n - 1) * t1)] / s)) / math.factorial(j)

    return q


main(a=[35, 31, 28, 40, 33, 35, 37, 35, 38, 32, 32, 35, 31, 34, 26, 23, 28, 24], s=40, k=3, c=50)

