all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build images and run the containers
	@[ -f .env ] || cp template.env .env
	@docker-compose build
	@docker-compose up -d

up: ## Start containers and run API BE project in dev mode
	@docker-compose start
	@docker-compose exec api-be ./run.sh

down: ## Stop containers
	@docker-compose stop

remove: ## Rmove all containers
	@docker-compose down

cmd: ## Command line of backend project
	@docker-compose exec api-be /bin/bash

restart: ## Restart all containers
	@docker-compose restart

.DEFAULT_GOAL := help