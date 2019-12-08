# Alt + F2 bookmarks F3 _ Shift F3
# Alt + ; metaGo
# cmnd + ` Terminal, Alt + Shift + U - Output
# Alt + 1,2,3 Jump to window
# Alt + \ Split window
# Alt + Shift + 2 navigate Right
# Alt + p Open file
# Alt + B Hide side bar
# Alt + shift + E Go to side bar
# Alt + Enter Add new line after
# Alt + Shift + Enter Add new line before

print(10 // 3)
print(10 % 3)

# Побитовые операции
# x | y ИЛИ
# x ^ y исключающее ИЛИ в случае двух переменных результат выполнения операции истинен тогда и только тогда, когда один из аргументов истинен, а другой — ложен
# x & y И
# x << y сдвиг влево
# x >> y вправо
# -x Инверсия

# Меняем местами значения 2-х переменных
a = 100
b = 200
a, b = b, a

x = y = 0 # immutable Неизменяемые объекты передаются по значению. (int, float, complex) (str) (tuple) 
x += 1
print(x, y)

x = y = [] # mutable Изменяемые объекты передаются по ссылке. (list) (set) (dict)
x.append(1)
x.append(2)
print(x ,y)

x = 2
print(1 < x < 3)

print(True and False)
print(True or False)
print(not False)

print(12 or False)
print(12 and "boom")

year = 2019
is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
print(is_leap)
