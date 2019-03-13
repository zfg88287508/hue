#!/bin/bash

set -e
set -x

BINDIR=$(dirname $0)
ROOT=${BINDIR%/*/*/*}
BUILD_LOG=/var/log/hue-build.log

DOCKER_REGISTRY=${DOCKER_REGISTRY:-"docker-registry.infra.cloudera.com/huecontainer"}
BASEOS="ubuntu1604"
BASEIMAGE="${BASEOS}:base"
BASEDOCKER=${DOCKER_REGISTRY}/${BASEIMAGE}

docker pull $BASEDOCKER 1>$BUILD_LOG 2>&1

WEBAPP_DIR=$BINDIR/container-build/webapp
HUE_SRC=$ROOT/hue
HUE_BLD=$ROOT/hue_build
mkdir -p $HUE_BLD

docker run -it -v $HUE_SRC:/hue -v $HUE_BLD:/hue_build $BASEDOCKER bash -c "cd /hue; make install"

#docker run -it -v $HUE_SRC:/hue -v $HUE_BLD:/hue_build $BASEDOCKER bash -c "./build/env/bin/pip install psycopg2-binary"

pushd .
cd $HUE_BLD/hue
GBN=$(curl http://gbn.infra.cloudera.com/)
WEBAPPIMAGE="webapp:$GBN"
docker build -f $WEBAPP_DIR/Dockerfile -t $WEBAPPIMAGE .
docker tag $WEBAPPIMAGE $DOCKER_REGISTRY/$WEBAPPIMAGE 
docker push $DOCKER_REGISTRY/$WEBAPPIMAGE
popd .
