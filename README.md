# portal

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Automatic classification of documents using percolator queries

## Getting Started

```sh
git clone git@github.com:KunihikoKido/portal.git
cd portal
make start
```

### Browsing

Web

* <http://localhost:8000/api/>
* <http://localhost:8000/admin/>

Kibana

* <http://localhost:5601/>

Elasticsearch

* <http://localhost:9200/>

## Commands

```sh
$make
usage: make [target] ...

targets:
help                        Show this help message.
build                       build docler containers
stop                        Stop docker containers.
status                      Status docker containers.
cli                         Run cli
tail                        Tail logs for docker containers
clean                       Clean docker containers and clean this project
start                       Start docker containers.
test                        Run tests
python.lint                 Run linter
django.version              Show django version
django.check                Run django check
django.test                 Run django tests
django.migrate              Ru migrate commands for django
django.makemigrations       Run makemigrations commands for django
django.dbshell              Run dbshell commands for django
django.shell                Run shell commands for django
django.createsuperuser      Run createsuperuser commands for django
django.loadusers            Load initial data
django.makemessages         Make messages
django.compilemessages      Compile messages
```
