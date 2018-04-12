.PHONY: build console run stop

build:
	docker-compose build

console: build
	docker-compose run -v $(PWD):/home/option_pricer -p 9090:9090 app /bin/bash

run:
	docker-compose up --build

stop:
	docker-compose down
