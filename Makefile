# Makefile for starting the docker container
SERVICE_NAME_LAB=sdn

start-docker:
	(. ./docker-sdn/setup-env.sh && docker compose up -d)

stop-docker:
	(. ./docker-sdn/setup-env.sh && docker compose down -v)

connect-docker: start-docker
	docker exec -it $(SERVICE_NAME_LAB) /bin/bash