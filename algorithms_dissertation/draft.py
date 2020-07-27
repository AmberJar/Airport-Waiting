iter = [1, 2, 3, 4.1, 5]
default_value = None
a = next((x for x in iter if x > 4), default_value)


if a:
    print('yes')

else:
    print('no')


print(2000 + 6000 + 600 + 3000 + 3000 + 2000)