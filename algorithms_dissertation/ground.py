import math
import datetime
import random
import csv
import numpy as np

starttime = datetime.datetime.now()

T = 20  # in hours

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
            P = 0
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

def total_waiting(a, s, k, c, Q):

    mean_time = SPVA(a, s, k, c, Q)

    total_delay = []
    for i in range(T):
        total_delay.append(mean_time[i] * a[i])

    #return total delay of each 18 hour (A 1 x 18 list)
    return total_delay


#heuristic
#optimization
def annealing(a, s, k, c, β, Q):

    iterations = 30    #iterations for each temperature
    α = 1               #airborne parameter
    #β = 1/60            #ground parameter
    global T             #全局变量T

    filename = 'heathrow.csv'

    with open(filename, 'rt') as csvfile:
        reader = csv.reader(csvfile, dialect='excel', delimiter=',')

        for row in reader:
            x = list(reader)
            aircraft_data = np.array(x, dtype='int')

    data_1 = list(aircraft_data[:, 1] / 100)
    data_0 = list(aircraft_data[:, 0] / 100)

    T0 = 10  # initial temperature
    T_min = 1 # minimum value of temperature

    # initialize plan
    best = a
    data_leave = data_1
    data_arrive = data_0

    # calculate initial result
    splitted = total_waiting(a, s, k, c, Q)
    w0 = sum(splitted)  # initial waiting time
    air_delay = w0 * α  # initial air delay cost
    ground_delay = 0  # initial ground delay cost
    d = []  # for writing
    temp = []  # for final comparison
    delay_hour = 0

    temp.append(a)
    temp.append(air_delay)

    #if the temperature is low enough, then exit
    while T0 >= T_min:

        iter = 1

        for i in range(iterations):

            d = []
            count_1 = 0

            while True:  # max number of aircraft of the final hour

                # if not changed for too many times, then leave the current iteration
                count_2 = 0

                while True:  # keep there is airplane can be delayed

                    if (random.random() >= 0.40 + iter * 0.004):
                        # find the most busy hour, randomly choose an hour that is the current one, the one before, or two hours before
                        t1 = int(splitted.index(max(splitted))) - random.choice([0, 1])

                        # if the selected hour is less than 0, then pick another one
                        while True:

                            if t1 >= 0 and t1 <= T - 2:
                                break

                            t1 = splitted.index(max(splitted)) - random.choice([0, 1])

                        # randomly choose number of hours to delay
                        t2 = random.choice([1, 2])

                        # after delay, if the current selected hour is over 17, then pick another delay hour
                        while True:

                            if t1 + t2 <= T - 1:
                                break

                            t2 = random.choice([1, 2])

                    else:
                        t1 = random.randint(0, T - 2)
                        t2 = random.choice([1, 2])
                        # generate a new arrangement in the neighborhood of x

                        while True:

                            if t1 + t2 <= T - 1:
                                break

                            t1 = random.randint(0, T - 2)
                            t2 = random.choice([1, 2])

                    allowed = 0

                    for i in range(len(data_arrive)):

                        if (data_arrive[i] >= t1 + 4 and data_arrive[i] < t1 + 5) and data_leave[i] >= 4:
                            allowed = i
                            break


                    if allowed:

                        data_arrive[allowed] = data_arrive[allowed] + t2
                        data_leave[allowed] = data_leave[allowed] + t2
                        break

                    else:
                        count_2 += 1

                    if count_2 >= 300:
                        break

                if count_2 >= 300:
                    break

                # copy the best plan to the current plan
                current = best[:]

                # change current plan with t1 and t2
                aircrafts = 1  # delay one aircraft in one time shows the best efficiency
                current[t1] = current[t1] - aircrafts
                current[t1 + t2] = current[t1 + t2] + aircrafts

                if current[T - 1] <= 30:
                    break

            if count_2 >= 300:
                break

            d.append(current)   #record current plan

            #generate new result
            w1 = sum(total_waiting(current, s, k, c, Q))       #current airborne delay

            #consider different cost function when delay
            cost = α * (w1 - w0) + (aircrafts * β * t2 * 60)  #calculate cost(may be other ways)
            print(cost)
            #delay hours
            hour = 0

            if cost < 0:
                w0 = w1
                best = current[:]
                ground_delay = ground_delay + aircrafts * β * t2 * 60
                delay_hour = delay_hour + t2

                d.append(α * w0)
                d.append(delay_hour)
                d.append(ground_delay)
                d.append(0)

            elif cost >= 0:
                #metropolis principle
                P = math.exp(-cost/T0)/iter
                r = random.random()
                print(P, r)
                if P > r:
                    w0 = w1
                    best = current[:]
                    ground_delay = ground_delay + aircrafts * β * t2 * 60
                    delay_hour = delay_hour + t2

                    d.append(α * w0)
                    d.append(delay_hour)
                    d.append(ground_delay)
                    d.append(0)
                else:
                    count_1 += 1

                    d.append(α * w0)
                    d.append(delay_hour)
                    d.append(ground_delay)
                    d.append(1)

            if count_1 >= 15:
                break

            print(d)
            iter += 1

        if count_2 >= 300:
            break

        T0 = 0.85 * T0



    temp.append(best)
    temp.append(w0)
    temp.append(delay_hour)
    temp.append(ground_delay)
    temp.append(k)
    temp.append(β)

    print(temp)

    return temp


#paramters definition
a = [6, 12, 36, 39, 35, 43, 42, 35, 36, 37, 39, 38, 37, 37, 38, 40, 38, 33, 16, 1]
s = 40
c = 30
fileHeader = ["Initial Plan", "Initial Cost", "Final Plan", "Final Cost", "Delay Hour", "Ground Delay Cost", "K",
              "belta"]
csvFile = open("data.csv", "w", newline='')
writer = csv.writer(csvFile)
writer.writerow(fileHeader)

for Q in [0]:

    for k in [1, 4, 7, 10]:

        for r in [1/24, 1/36, 1/48, 1/60]:

            A = annealing(a, s, k, c, r, Q)
            writer.writerow(A)

csvFile.close()

endtime = datetime.datetime.now()

print(endtime - starttime)






