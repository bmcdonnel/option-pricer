.PHONY: build console run stop

build:
	docker-compose build

console: build
	docker-compose run -v $(PWD):/home/option_pricer -p 8000:8000 app /bin/bash

run:
	docker-compose up --build

stop:
	docker-compose down
