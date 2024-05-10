FROM python:3.9-slim

RUN useradd -m -U -u 1000 proxyuser
USER proxyuser

WORKDIR /app
COPY --chown=proxyuser:proxyuser encrypted_dns_proxy.py .

EXPOSE 35353/udp
EXPOSE 35353/tcp

CMD ["python", "encrypted_dns_proxy.py"]
