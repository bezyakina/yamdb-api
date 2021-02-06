![Yamdb%20workflow](https://github.com/bezyakina/yamdb_final/workflows/Yamdb%20workflow/badge.svg)

# API Yamdb

Это групповой проект созданный на курсе Яндекс.Практикума, предоставляющий API для многопользовательской блог-платформы, разделенной по категориям, жанрам с возможностью добавления постов, отзывов и комментариев.

## Для начала работы

Клонируйте репозиторий из GitHub
```sh
$ git clone https://github.com/bezyakina/infra_sp2.git
$ cd infra_sp2
```
### Требования

Установите docker [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) и docker-compose [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Installing

Создайте файл`.env` с настройками среды Postgresql и секретным ключом.

Пример:
```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='secret-key'
```

Соберите и запустите контейнер
```
docker-compose up --build -d
```
Войдите в контейнер приложения ```web```
```
docker-compose exec web bash
```
Сделайте миграцию и наполните базу начальными данными
```
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata fixtures.json
```
Создайте суперпользователя
```
python manage.py createsuperuser
```
Выйдете из контейнера
```
exit
```

*Приложение работает на ваш-ip-адрес:1337/admin*
*Документация по API доступна на ваш-ip-адрес:1337/redoc*

## Запустите тесты
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```
## Технологии

**Django** [https://www.djangoproject.com/](https://www.djangoproject.com/) <br>
**Django Rest Framework** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/) <br>
**PostgreSQL** [https://www.postgresql.org/](https://www.postgresql.org/) <br>
**Docker** [https://www.docker.com/](https://www.docker.com/)

## Авторы

* **Безякина Елизавета** - [bezyakina](https://github.com/bezyakina)
* **Кокшаров Вадим** - [Vadim3x4](https://github.com/Vadim3x4)
* **Назарова Ирина** - [Irina-Nazarova](https://github.com/Irina-Nazarova)

## Лицензия
[MIT](LICENSE)
