#!/bin/bash

BASE_TAG=21.0.1

IMG_NAME=tilothiele/dolibarr:$BASE_TAG.1

docker build --build-arg BASE_TAG=$BASE_TAG -t $IMG_NAME .
docker push $IMG_NAME