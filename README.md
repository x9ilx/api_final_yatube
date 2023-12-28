# **yatube_api_final**
## **Описание**
Проект представляет собой API платформы YaTube.

YaTube социальная платформа, позволяющая:
- Создавать публикации;
- Комментировать публикации;
- Подписываться на авторов публикаций;

## **Установка**
Для запуска проекта необходимо:
1. Скачать файлы проекта.
2. Создать виртуальное окружение, коммандой в терминале
   ```python
   # Windows
   python -m venv venv
   
   # Linux
   python3 -m venv venv
   ```
3. Обновить "pip" и установить необходимые зависимости, коммандами в терминале
   ```python
   pip install --upgrade pip
   pip instal -r requirements.txt
   ```
4. Создать и применить миграции, предварительно перейти в дирректорию, содержащую файл manage.py, коммандами в терминале:
   ```python
   # Windows
   python manage.py makemigrations
   python manage.py migrate
   
   # Linux
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
6. Запустить локальный сервер, коммандой в терминале
   ```python
   cd yatube_api
   # Windows
   python manage.py runserver
   
   # Linux
   python3 manage.py runserver
   ```
7. Для запуска публичного сервера необходимо изменить настройки проекта yatube_api/settings.py. см. [документацию](https://docs.djangoproject.com/en/5.0/ref/settings/)
## **Примеры запросов к API**

### Получение публикаций

Получить список всех публикаций. При указании параметров limit и offset выдача должна работать с пагинацией.

QUERY PARAMETERS

>     limit: integer
> 
>     Количество публикаций на страницу
> 
>     offset: integer
> 
>     Номер страницы после которой начинать выдачу
 
### Responses 200

Удачное выполнение запроса без пагинации

### RESPONSE SCHEMA: application/json
> 
> Array
> 
>     id
> 
>     integer (id публикации)
> 
>     author: string (username пользователя)
> 
>     text: string (текст публикации)
> 
>     pub_date: string <date-time>
>
>     image: string or null <binary>
>
>     group: integer or null (id сообщества)


После запуска локального сервера подробная документация по API доступна по адресу: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/#tag/api)
