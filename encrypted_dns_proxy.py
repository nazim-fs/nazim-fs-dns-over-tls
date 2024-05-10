import socket
import ssl
import threading
import time

# Cloudflare as DOT server
upstream_dns_server = ('1.1.1.1', 853)
listening_address = '0.0.0.0'
listening_port = 35353

# Cache for DNS responses
dns_cache = {}

# Rate limiting parameters in seconds
max_requests = 10
request_window = 60

# Logging function to log messages inside `dns_proxy.log` file
def log_message(message, client_address=None, protocol='UDP'):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_str = f"[{timestamp}] {protocol} Request from {client_address}: {message}"
    with open('dns_proxy.log', 'a') as log_file:
        log_file.write(f'{log_str}\n')

def handle_dns_query(query_data):
    # Check cache for response
    if query_data in dns_cache:
        log_message(f"Cache hit: {query_data}")
        return dns_cache[query_data]

    # Rate limiting check
    global last_request_time, request_count
    current_time = time.time()
    if current_time - last_request_time > request_window:
        request_count = 0
        last_request_time = current_time

    if request_count >= max_requests:
        log_message("Rate limit exceeded.")
        return b'Rate limit exceeded.'

    request_count += 1
    log_message(f"Handling DNS query: {query_data}")

    # A new TLS connection to the CF DOT server
    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tls_socket:
        tls_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=upstream_dns_server[0])
        tls_socket.connect(upstream_dns_server)
        tls_socket.sendall(query_data)
        response = tls_socket.recv(1024)

        # Update cache
        dns_cache[query_data] = response

    return response

def handle_udp(udp_socket):
    while True:
        query_data, client_address = udp_socket.recvfrom(1024)
        response = handle_dns_query(query_data)
        udp_socket.sendto(response, client_address)
        log_message(query_data, client_address, 'UDP')

def handle_tcp(tcp_socket):
    while True:
        client_socket, client_address = tcp_socket.accept()
        query_data = client_socket.recv(1024)
        response = handle_dns_query(query_data)
        client_socket.sendall(response)
        client_socket.close()
        log_message(query_data, client_address, 'TCP')

def main():
    global last_request_time, request_count
    last_request_time = time.time()
    request_count = 0

    # A UDP socket creation to listen for DNS queries
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((listening_address, listening_port))

    # A TCP socket creation to handle DNS queries over TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((listening_address, listening_port))
    tcp_socket.listen(5)

    # A separate threads to start UDP and TCP handlers in
    udp_thread = threading.Thread(target=handle_udp, args=(udp_socket,))
    tcp_thread = threading.Thread(target=handle_tcp, args=(tcp_socket,))
    udp_thread.start()
    tcp_thread.start()

    udp_thread.join()
    tcp_thread.join()

    udp_socket.close()
    tcp_socket.close()

if __name__ == '__main__':
    main()

