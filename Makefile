build:
	docker compose -f local.yml up --build -d --remove-orphans

build-log:
	docker compose -f local.yml up --build   --remove-orphans

up:
	docker compose -f local.yml up -d

up-log:
	docker compose -f local.yml up 

down:
	docker compose -f local.yml down

down-v:
	docker compose -f local.yml down -v

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f rubico-local.yml logs app

makemigrations:
	docker compose -f local.yml run --rm app python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm app python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm app python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm app python manage.py createsuperuser

