#!/bin/bash

IMG_NAME=tilothiele/dolibarr:21.0.1

docker build -t $IMG_NAME .
docker push $IMG_NAME