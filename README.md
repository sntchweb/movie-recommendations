## Описание проекта
Проект представляет собой онлайн-платформу по рекомендациям и подбору фильмов по жанрам.  
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

***
# Backend

### Виртуальное окружение и зависимости:

Создать и активировать вирутальное окружение:

```bash
python -3.11 -m venv venv
source venv/Scripts/activate
```

Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Проброска порта для работы с бд:

В файле docker-compose.local.yml в разделе postgres_db сделать изменения.

```bash
  postgres_db:
    image: "postgres:13.4-alpine"
    env_file: devops.env
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - 5440:5432
```

### Запуск и сборка сети контейнеров docker:
Из директории /devops выполнить команду:
```bash
docker compose -f docker-compose.local.yml up --build
```

### Доступ к проекту:

При запущенной сети контейнеров, нужно будет зайти в контейнер, применить миграции и подгрузить статику.

```bash
cd devops
docker compose -f docker-compose.local.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.local.yml exec backend cp -r /app/static/. /static/static/
docker compose -f docker-compose.local.yml exec backend python manage.py migrate

```

Сайт будет доступен по адресам:
```bash
http://127.0.0.1/
http://localhost/
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
Django 4.2  
Django Rest framewrok 3.14  
Celery 5.3  
Redis 4.6  
PostgreSQL 13.4  
TypeScript  
CSS  

## Авторы проекта:
- Backend: Ибрагимов Рабадан, Лашин Артём, Ромашков Александр, Минаев Александр
- Frontend: Тимур Салахутдинов, Попов Дмитрий, Антон Лысцов, Мачехин Арсений, Винник Алексей
- QA: Анна Король, Роман Третьяков, Юлия Лукина, Макарьина Татьяна, Липчанов Андрей
- UI/UX: Кильсенбаева Айсылу, Александр Баранов
- SA: Смехова Ольга, Хохлов Влад
- DS: Евгений Прудовский
- PM: Гужиева Наталья
