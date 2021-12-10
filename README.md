## Решение [домашнего задания](https://github.com/netology-code/py-homeworks-web/tree/new/2.1-flask) к лекции «Flask»
1. Создано 2 таблицы: пользователи и посты/объявления
1. Доступные запросы:
    - получение всех постов - без авторизации
    - получение одного поста по id - без авторизации
    - создание пользователя - без авторизации
    - получение пользователя/авторизация по логину и паролю/получение токена
    - получение пользователя/авторизация по токену
    - создание поста/авторизация по токену или по логину и паролю
    - редактирование поста с проверкой авторства/авторизация по токену или по логину и паролю
    - удаление поста с проверкой авторства/авторизация по токену или по логину и паролю  
      
    Токен генерируется каждый раз, когда пользователь использует пароль, можно это вывести в отдельный запрос.
    Тогда решится вопрос с передачей токена пользователю, его можно будет передать в ответ.
    Сейчас токен просто выводится в консоль, оттуда его можно скопировать и использовать для выполнения запросов.  
    Файл с примерами запросов - [requests-examples.http](https://github.com/headsoft-mikhail/netology_flask/blob/master/requests-examples.http)
1. Методы авторизации вынесены в файл [authorization.py](https://github.com/headsoft-mikhail/netology_flask/blob/master/authorization.py)
1. Для выполнения миграций нужно запустить [migrate.sh](https://github.com/headsoft-mikhail/netology_flask/blob/master/migrate.sh).
[migrate.py](https://github.com/headsoft-mikhail/netology_flask/blob/master/migrate.py) помимо самих миграций создает базу данных, если она еще не создана.
1. Настройки проекта: логины, пароли, переменные для хэширования - в файле [config.py](https://github.com/headsoft-mikhail/netology_flask/blob/master/config.py)