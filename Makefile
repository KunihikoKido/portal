

.PHONY: help

help: ## Show this help message.
	@echo 'usage: make [target] ...'
	@echo
	@echo 'targets:'
	@egrep '^[a-z]+(.+)\:\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'


#----------------------------------------------------------
# Docker manage commands
#----------------------------------------------------------
.PHONY: build stop status cli tail clean start test

.docker.build:
	@docker-compose build
	@touch .docker.build

build: ## build docler containers
build:
	@$(MAKE) .docker.build

stop: ## Stop docker containers.
	@docker-compose stop

status: ## Status docker containers.
	@docker-compose ps

cli: ## Run cli
cli: build
	@docker-compose run --rm web bash

tail: ## Tail logs for docker containers
tail: build
	@docker-compose logs -f

clean: ## Clean docker containers and clean this project
	@docker-compose down --rmi all --volumes --remove-orphans
	@find . -name \*.pyc | xargs rm -rf
	@find . -name \*.build | xargs rm -rf
	@find . -name __pycache__ | xargs rm -rf
	@find . -name db.sqlite3 | xargs rm -rf

start: ## Start docker containers.
start: build django.migrate django.loadusers django.compilemessages
	@docker-compose up -d

test: ## Run tests
test: build python.lint django.test

#----------------------------------------------------------
# Python
#----------------------------------------------------------
.PHONY: python.lint

python.lint: ## Run linter
	@docker-compose run --rm web flake8


#----------------------------------------------------------
# Django commands
#----------------------------------------------------------
.PHONY: django.version django.check django.test django.makemigrations django.loadusers

django.version: ## Show django version
	@docker-compose run --rm web python -m django --version

django.check: ## Run django check
	@docker-compose run --rm web python manage.py check

django.test: ## Run django tests
django.test: django.check
	@docker-compose run --rm web python manage.py test

django.migrate: ## Ru migrate commands for django
	@docker-compose run --rm web python manage.py migrate

django.makemigrations: ## Run makemigrations commands for django
	@docker-compose run --rm web python manage.py makemigrations

django.dbshell: ## Run dbshell commands for django
	@docker-compose run --rm web python manage.py dbshell

django.shell: ## Run shell commands for django
	@docker-compose run --rm web python manage.py shell

django.createsuperuser: ## Run createsuperuser commands for django
	@docker-compose run --rm web python manage.py createsuperuser

django.loadusers: ## Load initial data
	@docker-compose run --rm web python manage.py loaddata fixtures/users.json

django.makemessages: ## Make messages
	@docker-compose run --rm web python manage.py makemessages -l ja

django.compilemessages: ## Compile messages
	@docker-compose run --rm web python manage.py compilemessages
