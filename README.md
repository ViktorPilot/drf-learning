 # Проект drf_learning

## Описание:

Проект drf_learning - это бэкенд-сервер, реализующий платформу для онлайн обучения, с возможностью размещения
пользовательских материалов и курсов.

## Стек используемых технологий (библиотек):
+ Python 3.12.10
+ poetry
+ django 6.0.4
+ djangorestframework 3.17.1
+ dotenv 0.9.9
+ pillow 12.3.0
+ psycopg2 2.9.12
+ python-dotenv 1.2.2
+ ipython 9.15.0
+ drf-yasg 1.21.15
+ stripe 15.4.0
+ Docker / Docker Compose
+ celery 5.6.3
+ redis 8.1.0
+ gunicorn 26.2.0
+ nginx
+ GitHub Actions
+ Docker Hub
Все контроллеры имеют способ определения и обработки представлений в DRF с помощью классов(метод CBV).

## Установка:

1. Клонируйте репозиторий:
    ```
     https://github.com/ViktorPilot/drf-learning.git
    ```
2. Запустите PyCharm у себя на компьютере.
3. Откройте скачанный репозиторий в PyCharm.
4. Создайте виртуальное окружение командой `poetry install`.
5. Активируйте ВО командой `poetry env activate`.
6. Установите зависимости командой `poetry init`.
7. Создайте и заполните файл `.env`.
8. Программа готова к работе.

## Настройка приложения:

1. Для запуска локального сервера у себя на компьютере необходимо в терминале ввести команду:
`python manage.py runserver 8000`(для Windows), `python3 manage.py runserver 8000`(для Unix-систем), 
где крайним значением указан порт запускаемого сервера.
2. Создайте миграции командой `python manage.py makemigrations`.
3. Примените миграции командой `python manage.py migrate`.
4. Загрузите фикстуры командами: 
- `python manage.py loaddata fixtures/materials/materials_fixture.json`
- `python manage.py loaddata fixtures/users/payments_fixture.json `
- `python manage.py loaddata fixtures/users/users_fixture.json`
- `python manage.py loaddata fixtures/users/groups.json`

## При работе через DOCKER:

1. Перед запуском установите Docker Desktop по ссылке `https://www.docker.com/products/docker-desktop` для WINDOWS, 
`https://docs.docker.com/engine/install/ubuntu/` для Linux.
2. Клонируйте репозиторий:
    ```
     https://github.com/ViktorPilot/drf-learning.git
    ```
3. Создайте и заполните файл .env.
4. Запустите Docker Compose `docker compose up --build`.
5. Проверьте состояние контейнеров `docker compose ps`.
6. При необходимости загрузки фикстур выполните:
- `docker compose exec web python manage.py loaddata fixtures/users/groups.json`
- `docker compose exec web python manage.py loaddata fixtures/users/users_fixture.json`
- `docker compose exec web python manage.py loaddata fixtures/materials/materials_fixture.json`
- `docker compose exec web python manage.py loaddata fixtures/users/payments_fixture.json `.
7. После запуска контейнера приложение доступно по адресу: `http://localhost:8000`.
8. Далее выполняйте работу с `materials` и `users`.

## Production-развертывание:

Production-развертывание выполняется с использованием Docker Compose, Docker Hub и GitHub Actions.
Production-конфигурация находится в: `docker-compose.prod.yaml`
Для production используются Docker-образы:
- `drf-learning`
- `drf-learning-nginx`

Образы собираются автоматически в GitHub Actions и публикуются в Docker Hub.
На сервере выполняется получение актуальных образов и запуск контейнеров через:
- `docker compose -f docker-compose.prod.yaml pull`
- `docker compose -f docker-compose.prod.yaml up -d`

Приложение работает за Nginx, который принимает внешние HTTP-запросы и передает их Django/Gunicorn.

## CI/CD:

Для автоматизации тестирования и развертывания используется GitHub Actions.
Workflow запускается автоматически при:
- `push`;
- `pull_request`.

Pipeline состоит из последовательных этапов: Test → Lint → Build → Deploy

### Test:

На этапе тестирования:
- запускается PostgreSQL;
- устанавливается Python;
- устанавливается Poetry;
- устанавливаются зависимости;
- выполняются Django migrations;
- запускаются тесты проекта.
При ошибке тестов pipeline останавливается.

### Lint:

После успешного прохождения тестов запускается Flake8: `poetry run flake8`.
При наличии ошибок линтера дальнейшие этапы не выполняются.

### Build:

После успешных тестов и линтера собираются Docker-образы:
- `drf-learning`
- `drf-learning-nginx`
После сборки образы отправляются в Docker Hub.

### Deploy:

После успешной сборки GitHub Actions подключается к production-серверу по SSH.
На сервере выполняются:

- `git pull`
- `docker compose -f docker-compose.prod.yaml pull`
- `docker compose -f docker-compose.prod.yaml up -d`

Таким образом, после успешного push новая версия приложения автоматически проходит тестирование, 
собирается в Docker-образы и разворачивается на сервере.

## Переменные окружения и Secrets:

Чувствительные данные не хранятся непосредственно в исходном коде.
Для локальной работы используется: .env

Шаблон переменных окружения находится в: .env.example

Секретные данные CI/CD хранятся в GitHub Secrets, в том числе:
- `SSH_KEY` — приватный SSH-ключ для подключения к серверу;
- `SSH_USER` — пользователь сервера;
- `SERVER_IP` — адрес сервера;
- `DOCKERHUB_USERNAME` — имя пользователя Docker Hub;
- `DOCKERHUB_TOKEN` — токен Docker Hub.

Файлы .env, виртуальные окружения, кэш Python и другие временные файлы исключены из Git с помощью .gitignore.

## Порядок работы с `materials` и `users`:

1. Реализована возможность создания, просмотра, редактирования и удаления курсов и уроков, используя 
API-запросы на локальный сервер.
2. Реализована возможность редактирования пользователей, используя API-запросы на локальный сервер.
3. Реализована возможность просмотра платежей пользователей.
4. Реализована возможность регистрации пользователей и получения ими токена для авторизации в приложении.
5. Реализована возможность распределения прав доступа в зависимости от статуса пользователя. Для модераторов разрешены 
права доступа с любыми уроками и курсами, но без возможности их удалять и создавать новые. Для пользователей, 
которые не входят в группу модераторов, разрешен просмотр, редактирование и удаление только своих курсов и уроков.
6. Реализована дополнительная проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com
7. Реализован эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.
8. Реализована пагинация для вывода всех уроков и курсов.
9. Каждый эндпоинт описан в документации с использованием drf-yasg.
10. Подключена возможность оплаты курсов через API.
11. Реализована рассылка писем пользователям при обновлении материалов курса не позднее четырех часов назад.
12. Реализовано блокирование пользователя при непосещении эндпоинтов проекта в течение месяца.

## Тестирование:

Данный проект покрыт юнит-тестами с использованием фреймворка rest_framework.test.
Для их запуска выполните команду `python manage.py test` из корневой директории проекта.

### Реализованы:

+ Тестирование корректности работы CRUD уроков.
+ Тестирование работы подписки на обновления курса.

## Документация:

Документация находится в стадии разработки, будет объявлена дополнительно.

## Лицензия:

Этот проект не лицензирован.