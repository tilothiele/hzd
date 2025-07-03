#!/bin/bash

BASE_TAG=21.0.1

IMG_NAME=tilothiele/dolibarr:$BASE_TAG

docker build --build-arg BASE_TAG=$BASE_TAG -t $IMG_NAME .
docker push $IMG_NAME