# Define variables
image_name = encrypted_dns_proxy_image
container_name = encrypted_dns_proxy_container
port = 35353

.PHONY: all deploy clean

all: deploy

deploy:
	@IMAGE_NAME=$(image_name) CONTAINER_NAME=$(container_name) PORT=$(port) ./deploy_proxy.sh

clean:
	@IMAGE_NAME=$(image_name) CONTAINER_NAME=$(container_name) PORT=$(port) ./cleanup_proxy.sh

