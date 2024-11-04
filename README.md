## FastAPI app с mailing микросервисом
Функционал простейший, суть была не в нем.
Оснвные цели:
* Реализовать async тесты с async движком у БД
* Прикрутить RabbitMQ
* Синхронизировать общейние 2х сервисов через Rabbit

(print -> ужас, TODO logging | loguru)
## Запуск

Необходимо создать и заполнить `.env` по примеру `.env.example`

В главной директории
```
make docker_up
```
Или
```
docker compose -f docker-compose.dev.yml up --buld -d
```

OpenAPI дока основного сервиса:
```
http://127.0.0.1:8000/api/docs
```
Rabbit:
```
http://127.0.0.1:15672/#/
```
mailing сервис без доки, там вообще нет эндпоинтов, просто должен отправлять письма.

### Для прогона тестов (которых мало, суть была async тесты прикрутить к FastAPI)
В главной директрории:
```
make docker_test_up
```
Или
```
sudo docker compose -f docker-compose.test.yml up -d
```
(Запуск тестовой БД в докере)

Установаить зависимости в директории ./app
```
poetry shell
```
```
poetry install
```

Запустить тесты из директории ./app
```
pytest
```
При необходимости в `pytest.ini` внести правки отображения.
В `pytest.ini` пробрасывается переменная окружения, чтобы шаффлить тестовую/локальную БД.
