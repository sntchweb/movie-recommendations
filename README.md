## Описание проекта
Проект представляет собой онлайн-платформу по рекомендациям фильмов.  
![Главная страница](https://github.com/sntchweb/movie-recommendations/blob/main/frontend/src/images/preview.jpg?raw=true)

## Что реализовано:
- Регистрация пользователей.
- Возможность оценки фильма.
- Возможность добавить фильм в избранное.
- Добавление фильма в список для просмотра.
- Выбор любимых жанров пользователя.
- Возможность выбрать аватарку пользователя.
- Расширенный поиск по фильмам с множественной фильтрацией (по жанру, стране, актеру, режиссеру, годам, рейтингу).
- Отправка сообщение на e-mail со ссылкой для подтверждения регистрации на платформе.

## Содержание

- [Первичные настройки: окружение/зависимости](#окружениезависимости)
- [Инициализация данных перед запуском контейнеров](#первоначальная-настройка-docker-compose)
- [Cборка контейнеров](#запуск-и-сборка-сети-контейнеров-docker)
- [Проброс порта для работы с Postgres в контейнере](#проброска-порта-для-работы-с-бд)
- [Доступ к проекту](#доступ-к-проекту)
- [Ручки/Схема API/Postman](#postmanimport-dataавтогерация-shema_apiyaml)
- [Код стайл проекта](#code-style)

***

# Backend

### Окружение/зависимости

В корне проекта **cd backend/** выполнить команды:

```bash
python -3.11 -m venv venv
source venv/Scripts/activate  #*unix - source venv/bin/activate
# (venv)...
# or
. venv/Scripts/activate
# (venv)...
```

Установка зависимостей:

```bash
pip install -r morec/requirements.txt
# or
cd morec/
pip install -r requirements.txt
```

***

### Первоначальная настройка docker compose

Запустить приложение docker desctop, или поднять машину через терминал.

```bash
cd devops
touch devops.env # поместить в файл devops.env данные из .env.example в корне проекта
```

***

### Запуск и сборка сети контейнеров docker

```bash
cd devops
docker compose -f docker-compose.local.yml down && docker compose -f docker-compose.local.yml up --build # команда подразумевает непрерывную работу с изменениями и постоянным сбросом контейнеров и пересборку. Если запуск осуществляется впервые, можно(не обязательно) отбросить первую часть команды до амперсандов(включительно &&(объеденяющая команда))
docker compose -f debug_in_container.yml up --build  # режим дэбага в контейнере(только если настроен собственный файл.yml под дэбаг)
docker compose -f debug_in_container.yml down
docker compose -f debug_in_container.yml down && docker compose -f debug_in_container.yml up --build
```

***

### Проброска порта для работы с бд

В файле docker-compose.local.yml в разделе postgres_db сделать изменения.

```bash
# ВНИАНИЕ! Эти настройки пишем только для себя, и перед пулл реквестом убираем, либо используем только в своей ветке.
# Не несем в прод!
  postgres_db:
    image: "postgres:13.4-alpine"
    env_file: devops.env
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - 5440:5432 # внутренний порт оставляем стандарт, а внешний, на свое усмотрение 5440 или другой.
```

Далее в pg admin или dbeaver создаем подключение к БД в котейнере:

```bash
# данные из .env для подключения postgres под управлением приложения.
Host = localhost
port = 5440  # или другой порта, в зависимости от шага выше
name_db = main_db
user = postgres
password = postgres
```

***

### Доступ к проекту

При запущенной сети контейнеров, нужно будет зайти в контейнер, применить миграции, и создать себе суперпользователя, также подгрузить статику.


```bash
cd devops
docker compose -f docker-compose.local.yml exec backend python manage.py migrate
docker compose -f docker-compose.local.yml exec backend python manage.py createsuperuser
docker compose -f docker-compose.local.yml exec backend python manage.py collectstatic
```

Сайт в полной мере доступен для разработки: http://localhost:80/

***

### Postman/import data/автогерация shema_api.yaml

Чтобы подтянуть схему Api и дергать ручки в проекте, необходимо установить специальную библиотеку, и сгенерирвоать файл.yaml, и в дальнейшем импортировать данные в Postman

Активировать окружение проекта, затем выполнить последовательность действий.

```bash
backend/# мы здесь
pip install pyyaml
cd morec/
python manage.py generateschema > schema.yaml
                                # имя файла на ваш вкус
```

В проекте появится файл schema.yaml, остается только импортировать в Postman файл, и можно приступать к тестированию.


***

### Code style

Установка линтеров:

```bash
pip install black isort flake8 flake8-isort
```

Настройки:
Создать файл **pyproject.toml** и наполнить:

```bash
[tool.black]
line-length = 79
skip-string-normalization = true
extend-exclude = 'tests|migrations'

[tool.isort]
profile = "black"
line_length = 79
src_paths = ["morec"]
extend_skip = ["tests", "migrations"]
```

Создать файл **setup.cfg** и наполнить:

```bash
[flake8]
ignore =
    W503,
    F811
exclude =
    tests/,
    */migrations/,
    venv/,
    env/
per-file-ignores =
    */settings.py:E501
max-complexity = 10
```

***

# Frontend
Установите все зависимости:
```bash
npm i --force
```
Для запуска:
```bash
npm start // localhost:3000
```

## Стек:
Python 3.11  
Django Rest framewrok 3.14  
Celery 5.3  
Redis 4.6  
PostgreSQL 13.4  
TypeScript  
CSS  
