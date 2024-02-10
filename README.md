# Блогикум

### Описание проекта:

На данном сайте пользователь может создать свою страницу и публиковать на ней сообщения («посты»).

Для каждого поста указывается категория, а также опционально локация, с которой связан пост.
Указав дату публикации «в будущем», можно создавать отложенные посты.
Они станут доступны всем посетителям с момента, указанного в поле «Дата».
Отложенные публикации доступны автору сразу же после отправки.

Пользователь может перейти на страницу любой категории и увидеть все посты, которые к ней относятся.
Пользователи могут заходить на чужие страницы, читать и комментировать чужие посты.

Авторизованные пользователи имеют возможность:
* создавать и комментировать публикации;
* редактировать собственные публикации и комментарии;
* удалять собственные публикации и комментарии.

### Как запустить проект:

Cоздать и активировать виртуальное окружение:

Windows
```
python -m venv venv
source venv/Scripts/activate
```
Linux/macOS
```
python3 -m venv venv
source venv/bin/activate
```

Обновить PIP:

Windows
```
python -m pip install --upgrade pip
```
Linux/macOS
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

Windows
```
python blogicum/manage.py migrate
```
Linux/macOS
```
python3 blogicum/manage.py migrate
```

Так же можно загрузить тестовые данные:

Windows
```
python blogicum/manage.py loaddata db.json
```
Linux/macOS
```
python3 blogicum/manage.py loaddata db.json
```

Запустить проект:

Windows
```
python blogicum/manage.py runserver
```
Linux/macOS
```
python3 blogicum/manage.py runserver
```
