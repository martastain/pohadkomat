scan:
	docker compose run --rm --remove-orphans pohadkomat python -m pohadkomat scan

chromecasts:
	docker compose run --rm --remove-orphans pohadkomat python -m pohadkomat chromecasts

next:
	docker compose run --rm --remove-orphans pohadkomat python -m pohadkomat next

build:
	docker build -t pohadkomat:latest .
