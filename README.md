# Как создать новый репозиторий

В локальном репозитории выполнить
```bash
git init
git add -A
git commit -m "First commit."
git remote add origin https://github.com/username/myproject.git
git push -u origin master
```
В команде git push мы использовали ключ -u. Данный ключ используется для того, чтобы связать локальную ветку master с удаленной origin/master

# Hotkeys для VScode
```python
# Alt + F2 bookmarks F3 _ Shift F3
# Alt + ; metaGo
# Alt +shift + t Terminal, Alt + Shift + U - Output
# Alt + 1,2,3 Jump to window
# Alt + \ Split window
# Alt + Shift + 2 navigate Right
# Alt + p Open file
# Alt + B Hide side bar
# Alt + shift + E Go to side bar
# Alt + Enter Add new line after
# Alt + Shift + Enter Add new line before
# Cmd + Shift + E - go to sidebar
# Alt + Shift + > - select right word
# Cmd + q - autocomplit (default alt+esc)
# Cmd + Shift + M - problem console


# unix
pip install virtualenv
# -m mod : run library module as a script (terminates option list)
python3 -m venv env
# source is a bash shell built-in command that executes the content of the file passed as argument, in the current shell. It has a synonym in . (period).
source env/bin/activate
deactivate

# windows
python3 -m venv c:\path\to\myenv
# Где вместо c:\path\to\myenv укажите путь до папки с виртуальным окружением, которую вы хотите создать.
# После того как скрипт отработает, вы можете активировать виртуальное окружение с помощью:
c:\path\to\myenv\Scripts\activate.bat
# Чтобы деактивировать виртуальное окружение:
c:\path\to\myenv\Scripts\deactivate.bat
```


# Примеры разметки на Github.com
----

## hello2

ававыа `выделение слова`

    Блок текста с более тёмным фоном

```python
print("Hello world!")
```
> Текст
> 
> Продолжение текста выделенного блока
> Завершение текста

1. Пункт 1
2. Пункт 2
3. Пункт 3

Название файла  | Содержание файла
----------------|----------------------
style.css       | Пустой файл каскадной таблицы стилей, в который производится сбока необходимых стилей
reset.css       | Reset CSS от Эрика Мейера
normalize.css   | Нормалайзер CSS от Nicolas Gallagher
block.css       | Основные стили блоков системы
addition.css    | Дополнительные стили
fontawesome.css | Стили иконочного шрифта
layout.css      | Основные стили, применительно к определённому сайту
lightbox.css    | Стили лайтбокса, если таковой используется
index.html      | Индексный файл для проверки вносимых изменений
