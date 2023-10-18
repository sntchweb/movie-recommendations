## Описание проекта
Проект представляет свобой онлайн-платформу по рекомендациям фильмов с возможностью регистрации, выставления оценок фильмов, добавления фильмов в список для просмотра.


![Главная страница сайта](https://github.com/sntchweb/movie-recommendations/blob/main/frontend/src/images/preview.jpg?raw=true)

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

В проекте используется Python версии 3.11

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
# ВНИАНИЕ! Эти настройки пишет только для себя, и перед пулл реквестом убираем, либо используем только в свое ветке/мастерской.
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

При запущенной сети контейнеров, нужно будет зайти в контейне, применить миграции, и создать себе суперпользователя, также подгрузить статику.

Вариант 1

```bash
# узнать имя контэйнера бэкенда
docker container ls
# пример:
    # devops-backend-1

# зайти в контейнер:
docker exec -it devops-backend-1 bash
# появится режим командной строки внутри контейнера:
# пример:
    # root@0450d15a0dd3:/app#

# Сначала применить миграции:
python manage.py migrate
# Затем создать суперюзера:
python manage.py createsuperuser
# Напоследок подгрузить статику:
python manage.py collectstatic
# 163 static files copied to '/app/collected_static'

# Выйти из режима контейнера
ctrl + D
```

Вариант 2

В этом случае нужно выполнить все те же команды выше начиная с миграции, но зайти в Docker Desktop, выбрать контейнер бэкенда из списка запущенный контейнеров, и перейти в раздел Terminal, далее накатить миграции, создать суперюзера, и выгурзить статику.

Вариант 3 (Pro)

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

**Внимание!** Не тащить установленную библиотеку **pyyaml** в зависимости проекта!

***

### Code style

Установка линтеров:

```bash
pip install black isort flake8 flake8-isort # можно пользоваться ruff, по желанию.
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

Запуск линтеров, пример:

```bash
# Ниже приведет запуск black при условии что конфигурационные файлы в проекте не прописаны:
black -S -l 79 morec/. # проверит и приведет в порядок все файлы в папке morec/. Где флаг -S отключение замены на двойные ковычки, а флаг -l 79 отвечает за макс длинну символов кода в проекте. Путь - morec/, а точка в конце, как указание, проверить всю директорию.

#Если конфигурационные файлы прописаны, то достаточно прописать так:
black morec/.

isort morec/. # приведет впорядок иморты
# or
isort .

# проверка
flake8 .
```

**Внимание!** Не тащить установленные библиотеки в зависимости проекта, а также конфигурационные файлы для линтеров в репозиторий! Пропишите собственный gitignore или подкидывайте в проект конфигурационные файлы, когда нужно привести код в порядок.

Пример. Правили код в **movies.py**, тогда правим и импорты или код-стайл допустим в backend/morec/api/views/movies.py

```bash
backend/  # находимся тут
black morec/api/views/movies.py  # приведет код в порядок
isort morec/api/views/movies.py  # поправит импорты
flake8 morec/api/views/movies.py  # удостовериться что все впорядке/можно в начале запустить эту команду, и понять сразу, нужно ли применять линтеры.
```

***

# Frontend
Прежде всего установите все зависимости:
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
PostgreSQL  