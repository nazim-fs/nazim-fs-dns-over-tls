#!/bin/bash

# Stop and remove the proxy container
docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME

# Remove the proxy image
docker rmi $IMAGE_NAME:latest

