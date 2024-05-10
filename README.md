# DNS to DNS over TLS Proxy:

## Introduction:

This DNS over TLS proxy implementation offers secure and efficient DNS resolution, utilizing Python's threading capabilities to communicate securely with Cloudflare's DNS-over-TLS (DoT) server. It features rate limiting, caching, and detailed logging, making it a versatile solution for secure DNS resolution across diverse network environments.


## Implementation & Achievements:

1. DNS Query Handling:
   - Handles DNS queries and responds to both UDP and TCP clients.
   - Establishes a secure TCP connection with Cloudflare's DoT server for DNS resolution.
   - Implements rate limiting, caching, and logging functionalities.
2. Multi-protocol Support:
   - Works over TCP and UDP, providing secure DNS resolution over TCP while handling UDP requests.
3. Rate Limiting, Caching, and Logging:
   - Implements rate limiting to prevent abuse, caching for improved performance, and detailed logging for monitoring and debugging.


## Additional queries:

### Imagine this proxy being deployed in an infrastructure. What would be the security concerns you would raise?
- This setup acknoweldges the fact that its not perfect, hence it also acknoweldges following security concerns associated with it:
   - Making sure our communications are secure, like using encryption so no one can spy on what we're doing.
   - Keeping an eye on how much traffic we're getting and slow things down if it gets too much.
   - Keeping everything updated so we're protected from known issues.

### How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?
- There are various ways to integrate this solution in a distributed architecture, such as below:
  - Since proxy is already containerized, it's easy to move around and manage it, especially if we're using any container orchestration tools such as Kubernetes.
  - Spreading out the work evenly using utilties such as load balancing, so not one server gets overloaded.
  - Making sure we can add more servers quickly if we need to handle more traffic.

### What other improvements do you think would be interesting to add to the project?
- There is still a room for an improvements in this setup, such as below to name a few:
  - Adding support for DNS filtering and blocking of malicious domains or unwanted content.
  - Integrating metrics and monitoring tools to gather performance data and monitoring the health of the DNS proxy.
  - Handling cases when our main server is down.
  - Making it easy to change settings without touching code.


## Pre-requisites:

To successfully deploy the proxy, the following pre-requisites must be satisfied:

- port `35353` availability.
- `docker` installed on the machine.
- Utilities such as `ncat`, `nslookup`, `tcpdump`, `dig` to be available & intalled on the machine to test or troubleshoot the proxy issues.
- `make` utility.


## Deployment Procedure:

Deploying the proxy involves building and running the Docker container. Simply run following command to achieve it:
```
make deploy
```


## Testing Procedure:

Upon successful deployment, you may use tools such as `nslookup`, `host`, `dig` as below to test the proxy:
```
nslookup -port=35353 -type=A -vc google.com localhost
dig @localhost -p 35353 +tcp google.com
echo -n "google.com" | ncat localhost 35353
host -T -p 35353 google.com localhost
```


## Cleanup procedure:

Cleaning up is as simple as deployment. Execute following command to cleanup the underlying resources:
```
make clean
```


## Possible Troubleshooting:

- This setup assumes running on port `35353` since port `53` conflicts with the DNS running on linux machines. Please make sure that port `35353` is not already being used.
- If you see connection refused errors as below, please make sure that the proxy container is up & running and listening on port `35353`:
```
$ dig @localhost -p 35353 +tcp google.com
;; Connection to 127.0.0.1#35353(127.0.0.1) for google.com failed: connection refused.
;; Connection to 127.0.0.1#35353(127.0.0.1) for google.com failed: connection refused.
;; Connection to 127.0.0.1#35353(127.0.0.1) for google.com failed: connection refused.
```
- Following commands can also be used to troubleshoot any issues:
```
$ docker inspect --format='{{json .NetworkSettings.Ports}}' encrypted_dns_proxy_container
$ openssl s_client -connect localhost:35353
$ sudo tcpdump -i any udp port 35353
$ sudo tcpdump -i any tcp port 35353
```


## Reference links:

- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#additional-resources)
- [Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [CloudFlare DNS over TLS](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-tls/)
- [IETF](https://datatracker.ietf.org/doc/html/rfc7858)

 
