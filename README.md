# Foodgram
- Доступен по адресу: http://51.250.2.201/
- Админ панель: http://51.250.2.201/admin/
- Спицификация API: http://51.250.2.201/api/docs/

## Технологии
- Python
- Django
- Django REST Framework
- PostgreSQL
- Nginx
- Gunicorn
- Docker
- GitHub Actions
- Yandex.Cloud

## Описание проекта
Пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Setup для работы с удаленным сервером (на ubuntu):
Выполните вход на свой удаленный сервер
```
ssh <username>@<ip>
```
Установите docker на сервер:
```
sudo apt install docker.io 
```
Установите docker-compose на сервер:
```
sudo apt install docker-compose
```
Клонируйте репозиторий
```
git clone git@github.com:dimabaril/foodgram-project-react.git
```
Перейдите в каталог infra.   
Cоздайте .env файл и наполните его:
```
cd infra
```
```
DJANGO_SECRET_KEY=<секретный ключ>
DB_ENGINE=django.db.backends.postgresql  # указываем, что работаем с postgresql
DB_NAME=<имя базы данных>
POSTGRES_USER=<логин для подключения к базе данных>
POSTGRES_PASSWORD=<пароль для подключения к БД>
DB_HOST=<название сервиса (контейнера)>  # db
DB_PORT=<порт для подключения к БД>  # 5432
```
  
Находясь в папке infra поднимите контейнеры:
```
sudo docker-compose up -d --build
```
После успешной сборки на сервере зайдем в контейнер backend и выполним следющие команды(выполняются один раз, далее созданное живёт на сервере):  
Зайдем в контейнер backend(далее команды выполним в нём):
```
sudo docker-compose exec backend bash
```
Соберите файлы статики:
```
python manage.py collectstatic
```
Примените миграции:
```
python manage.py migrate
```
Загрузите ингридиенты в базу данных:  
```
python manage.py importcsv
```
Создать суперпользователя Django:
```
python manage.py createsuperuser
```
### !!! Обязательно зайдите в панель администратора и создайте хотя бы пару тегов, без этого ничего не заработает.!!!
## Setup на локальной машине:
Отличается тем что заходить не надо и Docker скорее всего у вас уже установлен.
## Ура всё работает!!!
## Автор:
Дмитрий Барилкин

