import math
import datetime
import random
import csv
starttime = datetime.datetime.now()

T = 20  # in hours

def SPVA(a, s, k, c):
    P = 0

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
    q_length = []

    for i in range(0, t):

        mean_ql = 0
        awt = 0

        for j in range(0, c + 1):

            mean_ql = mean_ql + Matrix[i][j] * j

        q_length.append(mean_ql)

    hour_q_length =[]
    results = [] #AWT hourly

    for i in range(0, T):

        hour_q = 0

        for j in range(s):

            hour_q = hour_q + q_length[s * i + j]

        hour_q_length.append(hour_q / 60)

        hour_queue = hour_q / 60
        hour_awt = (hour_queue + 0.5) * 1.5
        results.append(hour_awt)

    #return the results of average delay in different hours
    return results


def binco(k, j):
    q = math.factorial(k - 1 + j)/(math.factorial(j) * math.factorial(k - 1))

    return q


def join(a, s, t1, n, j, k):
    q = binco(k, j) * (a[math.floor((n - 1) * t1)] ** j) * (k * s) ** k / (a[math.floor((n - 1) * t1)] + k * s) ** (k + j)
    return q



#based on funtion before
#calculate the total waiting time in each hour

def total_waiting(a, s, k, c):

    mean_time = SPVA(a, s, k, c)

    total_delay = []
    for i in range(T):
        total_delay.append(mean_time[i] * a[i])

    #return total delay of each 18 hour (A 1 x 18 list)
    return total_delay

#heuristic
#optimization
def annealing(a, s, c):

    iterations = 60    #iterations for each temperature
    α = 1               #airborne parameter
    #β = 1/60            #ground parameter

    fileHeader = ["index", "airborne delay cost", "ground delay cost", "transform"]
    csvFile = open("file.csv", "w", newline='')
    writer = csv.writer(csvFile)
    writer.writerow(fileHeader)

    #current best plan
    best_results = []

    for k in [1, 4, 7, 10, 13]:

        for β in [1/24, 1/36, 1/48, 1/60]:

            T = 5  # initial temperature
            T_min = 0.2 # minimum value of temperature
            best = a # initialize plan
            # calculate initial result
            w0 = sum(total_waiting(a, s, k, c))  # initial waiting time
            air_delay = w0 * α  # initial air delay cost
            ground_delay = 0  # initial ground delay cost
            d = []  # for writing
            temp = []  # for final comparison
            delay_hour = 0
            # writing
            d.append(a)
            d.append(air_delay)
            d.append(delay_hour)
            d.append(0)
            writer.writerow(d)

            temp.append(a)
            temp.append(air_delay)

            #record the hour that already has delayed
            delay_status = [0] * 20

            #if the temperature is low enough, then exit
            while T >= T_min:

                #if not changed for too many times, then leave the current iteration
                counter = 0

                for i in range(iterations):

                    d = []

                    if (random.random() >= 0.60 - iterations * 0.004):
                        #find the most busy hour, randomly choose an hour that is the current one, the one before, or two hours before
                        t1 = int(best.index(max(best))) - random.choice([0, 1])

                        #if the selected hour is less than 0, then pick another one
                        while True:

                            if t1 >= 0 and t1 <= 18:
                                break

                            t1 = best.index(max(best)) - random.choice([0, 1])

                        #randomly choose number of hours to delay
                        t2 = random.choice([1, 2])

                        #after delay, if the current selected hour is over 17, then pick another delay hour
                        while True:

                            if t1 + t2 <= 19:
                                break

                            t2 = random.choice([1, 2])
                    else:
                        t1 = random.randint(0, 19)
                        t2 = random.choice([1, 2])
                        # generate a new arrangement in the neighborhood of x

                        while True:

                            if t1 + t2 <= 19:
                                break

                            t1 = random.randint(0, 19)
                            t2 = random.choice([1, 2])

                    #copy the best plan to the current plan
                    current = best[:]

                    #change current plan with t1 and t2
                    aircrafts = 1   #delay one aircraft in one time shows the best efficiency
                    current[t1] = current[t1] - aircrafts
                    current[t1 + t2] = current[t1 + t2] + aircrafts

                    d.append(current)   #record current plan

                    #generate new result
                    w1 = sum(total_waiting(current, s, k, c))       #current airborne delay

                    #consider different cost function when delay
                    cost = α * (w1 - w0) + (aircrafts * β * t2 * 60) * (1 + delay_status[t1] * 0.3)  #calculate cost(may be other ways)

                    #delay hours
                    hour = 0

                    if cost < 0:
                        print(delay_hour)
                        w0 = w1
                        best = current[:]
                        ground_delay = ground_delay + aircrafts * β * t2 * 60 * (1 + delay_status[t1] * 0.3)
                        delay_hour = delay_hour + 1
                        delay_status[t1] = delay_status[t1] + 1

                        d.append(α * w0)
                        d.append(delay_hour)
                        d.append(0)

                    elif cost >= 0:
                        #metropolis principle
                        P = math.exp(-cost/T)
                        r = random.random()

                        print(P,r)
                        print(delay_hour)

                        if P > r:
                            w0 = w1
                            best = current[:]
                            ground_delay = ground_delay + aircrafts * β * t2 * 60 * (1 + delay_status[t1] * 0.3)
                            delay_hour = delay_hour + 1
                            delay_status[t1] = delay_status[t1] + 1

                            d.append(α * w0)
                            d.append(delay_hour)
                            d.append(0)
                        else:
                            counter = counter + 1

                            d.append(α * w0)
                            d.append(delay_hour)
                            d.append(1)


                    writer.writerow(d)
                    print(d)

                    if counter >= 15:
                        break

                T = 0.9 * T


            temp.append(best)
            temp.append(w0)
            temp.append(ground_delay)
            temp.append(k)
            temp.append(β)

            print(temp)

    csvFile.close()

    return temp


#paramters definition
a = [6, 12, 36, 39, 35, 43, 42, 35, 36, 37, 39, 38, 37, 37, 38, 40, 38, 33, 16, 1]
s = 40
c = 50

A = annealing(a, s, c)

endtime = datetime.datetime.now()

print(endtime - starttime)






