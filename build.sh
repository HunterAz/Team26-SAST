#!/bin/sh
NGINX_DOCKER=meok_nginx
FLASK_DOCKER=meok_flask
MYSQL_DOCKER=meok_mysql

FRONTEND_NETWORK=meok_frontend
BACKEND_NETWORK=meok_backend

NGINX_FOLDER="$PWD/nginx/"
FLASK_FOLDER="$PWD/flask/"
MYSQL_FOLDER="$PWD/mysql/"

# Remove all containers: docker rm -f `docker ps -aq`
# remove containers if exists
if docker ps -a | grep -q $NGINX_DOCKER; then
	docker rm -f $NGINX_DOCKER
fi
if docker ps -a | grep -q $FLASK_DOCKER; then
	docker rm -f $FLASK_DOCKER
fi
if docker ps -a | grep -q $MYSQL_DOCKER; then
	docker rm -f $MYSQL_DOCKER
fi

# front end network
if docker network ls | grep -q $FRONTEND_NETWORK; then
	docker network rm $FRONTEND_NETWORK
fi
docker network create $FRONTEND_NETWORK

# back end network
if docker network ls | grep -q $BACKEND_NETWORK; then
	docker network rm $BACKEND_NETWORK
fi
docker network create $BACKEND_NETWORK

# nginx container
docker image build $NGINX_FOLDER -t $NGINX_DOCKER
docker run -d  \
        --name $NGINX_DOCKER \
        --volume "${NGINX_FOLDER}logs":"/var/log/nginx/" \
        --user 1000:1000 \
        --publish 80:80 \
        --publish 443:443 \
        --network $FRONTEND_NETWORK \
        $NGINX_DOCKER

# flask container
docker image build $FLASK_FOLDER -t $FLASK_DOCKER
docker run -d  \
	--name $FLASK_DOCKER \
	--volume "${FLASK_FOLDER}website":"/home/meok/website" \
	--env-file "${FLASK_FOLDER}.env" \
	--network $FRONTEND_NETWORK \
	$FLASK_DOCKER
# can only connect to 1 network at a time
docker network connect $BACKEND_NETWORK $FLASK_DOCKER

# mysql container
docker image build $MYSQL_FOLDER -t $MYSQL_DOCKER
docker run -d  \
	--name $MYSQL_DOCKER \
	--volume "${MYSQL_FOLDER}database_data":"/var/lib/mysql" \
	--env-file "${MYSQL_FOLDER}.env" \
	--network $BACKEND_NETWORK \
	$MYSQL_DOCKER \
	mysqld --default-authentication-plugin=mysql_native_password
