#!/bin/bash

# Build the proxy image
docker build -t $IMAGE_NAME .

# Run the proxy container
docker run -d -p $HOST_PORT:$CONTAINER_PORT/udp -p $HOST_PORT:$CONTAINER_PORT/tcp --name $CONTAINER_NAME $IMAGE_NAME

