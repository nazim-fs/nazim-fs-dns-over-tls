# Variables
image_name = encrypted_dns_proxy_image
container_name = encrypted_dns_proxy_container
host_port = 35353
container_port = 53

.PHONY: all deploy clean

all: deploy

deploy:
	@IMAGE_NAME=$(image_name) CONTAINER_NAME=$(container_name) HOST_PORT=$(host_port) CONTAINER_PORT=$(container_port) ./deploy_proxy.sh

clean:
	@IMAGE_NAME=$(image_name) CONTAINER_NAME=$(container_name) ./cleanup_proxy.sh

