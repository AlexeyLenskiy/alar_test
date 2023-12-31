postgres:
	docker run --name postgres15 -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=password -d postgres:15.3-alpine

startpostgres:
	docker start postgres15

build:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

test:
	docker-compose run app pytest .