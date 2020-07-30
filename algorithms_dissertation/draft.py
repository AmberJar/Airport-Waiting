import csv as csv
import numpy as np

filename = 'heathrow.csv'

with open(filename, 'rt') as csvfile:
    reader = csv.reader(csvfile, dialect='excel', delimiter=',')

    for row in reader:

        x = list(reader)
        data = np.array(x, dtype='int')

    print(data)
    print(data[100,0])
iter = [1, 2, 3, 4.1, 5]
default_value = None
a = next((x for x in iter if x > 4), default_value)


if a:
    print('yes')

else:
    print('no')


print(2000 + 6000 + 600 + 3000 + 3000 + 2000)