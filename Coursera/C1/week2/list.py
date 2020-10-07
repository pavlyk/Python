col = ['list', 'tuple', 'dict', 'set']

print(len(col), col[0], col[-1])

col[3] = 'frozentset'

print(col)

print(col[0:2])

print(col[::2])

# При срезе создается новый объект
print(col[:] is col)

# Нумерация
for idx, coll in enumerate(col):
    print('#{} {}'.format(idx, coll))

col.append('OrderedDict')

col += ['OrderedDict2']

print(col)

print(', '.join(col))

import random

rl = []
for i in range(10):
    rl.append(random.randint(1, 20))

print(rl)

# sorted возвращается новый
print(sorted(rl))

# sort именяет
rl.sort()
print(rl)

# Кортежи

immutables = ([1,2] ,2 ,3)
immutables[0].append(3)

print(immutables)