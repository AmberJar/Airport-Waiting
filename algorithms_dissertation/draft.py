import numpy as np
i = 100
while i > 0.01:

    if i < 0.8:
        continue

    i = np.random.random()
    print(i)

