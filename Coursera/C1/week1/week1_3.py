# Управление потоком

company = "my.com"

if "my" in company:
    print("ok")

if (2==1 or 3==3):
    print("ok")

if False:
    print(1)
elif True:
    print(2)
else:
    print(3)

winner = "Argentina" if 3 > 2 else "Jamaica"

print(winner)

i = 0
while i < 10:
    print(i)
    i += 1

for n in range(11):
    print(n)

for m in range(10, 1, -2):
    print(m)

for i in range(10):
    pass

while True:
    print("break")
    break