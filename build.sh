#!/bin/bash

set -e


function build() {
  docker build . -f ./compose/$1/Dockerfile -t foxhound_$1
}

build web
build nginx
build frontend

docker-compose -f ./compose/docker-compose.yml up --no-deps --force-recreate --remove-orphans -d web frontend nginx