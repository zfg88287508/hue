#!/bin/bash

set -e
set -x

BINDIR=$(dirname $0)
HUE_ROOT=$PWD

DOCKER_REGISTRY=${DOCKER_REGISTRY:-"docker-registry.infra.cloudera.com/huecontainer"}
BASEOS="ubuntu1604"
BASEIMAGE="${BASEOS}:base"
BASEDOCKER=${DOCKER_REGISTRY}/${BASEIMAGE}
BUILD_LOG=/var/log/hue-build.log

docker build -t $BASEDOCKER . 1>$BUILD_LOG 2>&1
docker tag $BASEDOCKER $BASEIMAGE
docker tag $BASEDOCKER $BASEOS
docker push $BASEDOCKER 1>$BUILD_LOG 2>&1
