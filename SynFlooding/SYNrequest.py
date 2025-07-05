from scapy.all import IP, TCP, Raw, send
from ipaddress import IPv4Address
from random import getrandbits
from urllib.parse import urlsplit, SplitResult
import socket

class SYNrequest:
    def __init__(self, url):
        self.url: str = url
        parsed: SplitResult = urlsplit(url)

        # Get hostname and port from parsed URL
        hostname = parsed.hostname
        port = parsed.port

        if not hostname:
            raise ValueError("Invalid URL: Could not extract hostname")

        try:
            self.ip = IPv4Address(socket.gethostbyname(hostname))
        except Exception as e:
            raise ValueError(f"Failed to resolve hostname '{hostname}' to IP: {e}")

        # Default ports
        if port is None:
            if parsed.scheme == 'http':
                self.port = 80
            elif parsed.scheme == 'https':
                self.port = 443
            else:
                raise ValueError(f"Unsupported or missing scheme: '{parsed.scheme}'")
        else:
            self.port = port

        self.tcp = TCP(dport=self.port, sport=getrandbits(16), flags='S', seq=getrandbits(32))
        self.pkt = IP(dst=str(self.ip)) / self.tcp / Raw(b"X"*1024)

    def send(self):
        try:
            if self.port == 80:
                self.http_request()
            elif self.port == 443:
                self.https_request()
            else:
                self.generic_request()
        except Exception as e:
            print(f'Error: {e}')

    def http_request(self):
        send(self.pkt, verbose=False)
        print(f'Sent SYN packet to {self.ip} on port {self.port} (HTTP)')

    def https_request(self):
        send(self.pkt, verbose=False)
        print(f'Sent SYN packet to {self.ip} on port {self.port} (HTTPS)')

    def generic_request(self):
        send(self.pkt, verbose=False)
        print(f'Sent SYN packet to {self.ip} on port {self.port} (custom)')
