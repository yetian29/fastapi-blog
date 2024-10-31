APP_FILE=docker-compose/app.yaml
STORAGES_FILE=docker-compose/storages.yaml


.PHONY:

lint:
	poetry run ruff check --fix .

format:
	poetry run ruff format .

up_app:
	docker-compose --env-file .env -f ${APP_FILE} -f ${STORAGES_FILE} up --build

down_app:
	docker-compose -f ${APP_FILE} -f ${STORAGES_FILE} down


all: lint format up_app 