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