from client import Client
from server import Server

def main() -> None:
    server = Server()
    client = Client()
    
    server.listen()
    client.connect()
    
if __name__ == '__main__':
    main()