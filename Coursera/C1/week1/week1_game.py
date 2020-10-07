import random
print("hello")

num = random.randint(0,101)

while True:
    answer = input("Введите число: ")
    if not answer or answer == "exit":
        break

    if not answer.isdigit():
        print("Введите правильное число")
        continue

    user_answer = int(answer)

    if user_answer > num:
        print("Загаданное число меньше")
    elif user_answer < num:
            print("Загаданное число больше")
    else:
        print('Good!')
        break