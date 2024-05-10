#!/bin/bash

# Build the proxy image
docker build -t $IMAGE_NAME .

# Run the proxy container
docker run -d -p $PORT:$PORT/udp -p $PORT:$PORT/tcp --name $CONTAINER_NAME $IMAGE_NAME

