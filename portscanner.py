import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def scan_port(target_host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout to 1 second
        sock.settimeout(1)
        # Connection attempt
        result = sock.connect_ex((target_host, port))
        # Open port check
        if result == 0:
            return port
        else:
            return None
        # Close the socket
        sock.close()
    except KeyboardInterrupt:
        print("Scan stopped by user.")
        exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        exit()
    except socket.error:
        print("Couldn't connect to server.")
        exit()

def generate_report(open_ports):
    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(f"Port {port}")
    else:
        print("No open ports found.")

def main():
    parser = argparse.ArgumentParser(description="Simple port scanner")
    parser.add_argument("host", help="Target host to scan")
    parser.add_argument("-p", "--ports", nargs="+", type=int, default=[i for i in range(1, 1025)],
                        help="Ports to scan (default: 1-1024)")
    args = parser.parse_args()

    target_host = args.host
    ports = args.ports

    if is_valid_ip(target_host):
        ip_address = target_host
    else:
        ip_address = resolve_hostname(target_host)
        if ip_address is None:
            print("Invalid hostname or hostname could not be resolved.")
            exit()

    print(f"Scanning host {target_host} ({ip_address})...\n")

    open_ports = []

    # This will speed up the scanning process
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scan_port, ip_address, port): port for port in ports}
        for future in futures:
            port_result = future.result()
            if port_result:
                open_ports.append(port_result)

    generate_report(open_ports)

if __name__ == "__main__":
    main()
