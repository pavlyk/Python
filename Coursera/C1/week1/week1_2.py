
x = 300
y = 300
print(id(x))
print(id(y))
# оператор == проверяет равенство значений двух объектов
# оператор is проверяет идентичность самих объектов.
# Его используют, чтобы удостовериться, что переменные указывают на один и тот же объект в памяти
# print(a == b)
print(x is y)

example_string = "Курс \"python\""

print(type(example_string))
print(example_string)

example_string = r"Файл на диске c:\\" # Сырая строка
print(example_string)

# Разбить длинную строку

example_string = "Первая строка" \
                "Вторая строка"

print(example_string)

print("Умножение строк "*3)

# Строки не изменяемые
example_string = "Hi"
print(id(example_string))
example_string += "!"
print(id(example_string))

print(example_string[1:])

example_string = "1234567890"

print(example_string[::2])
print(example_string[::-1])

quote = "Болтовная ничего не стоит. Покажи мне код. (с) Linus Torvalds"

print(quote.count("о"))

print("moscow".capitalize())

print("2019".isdigit())

print("hello" in "world hello!!1!")

example_string = "hello!"

for letter in example_string:
    print(letter)

num_string = str(999.01)
print(type(num_string))

template = "{} главное достоинство программиста!".format("Лень")

print(template)

subject = "оптимизация"
author = "Donald Knuth"

print(f"Преждевременная {subject} - корень всех зол. ({author})")

num = 8
print(f"Binary: {num:#b}")

num = 2/3

print(f"{num:#.3f}")

# name = input("Введите имя ")
# print(name)

example_string = b"hello"
print(type(example_string))

for elements in example_string:
    print(elements)

example_string = "привет"

encoded_str = example_string.encode(encoding="utf-8")
print(encoded_str) # d0 bf - кодировка символа "п"

decoded_str = encoded_str.decode()
print(decoded_str)

answer = None

print(bool(None))

