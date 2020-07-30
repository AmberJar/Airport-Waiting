data = [1, 2, 3.1, 3, 5, 4 ,6]
default = None

a = next((x for x in data if (x >= 3 and x < 4)), default)

print(a)