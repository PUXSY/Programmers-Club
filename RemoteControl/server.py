import threading
import socket
import time
from info import Global_Vribols
import sys

GV = Global_Vribols()
ADRR = GV.ADRR()
DISCONNECT_MESSAGE = "DISCONNECT"

class Server:
    def __init__(self) -> None:
        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADRR)
        self.running = True
       
    def handle_client(self, conn: socket.socket, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True  
        while connected:
            try:
                msg_len = conn.recv(1024).decode()
                if msg_len:
                    msg_len = int(msg_len)
                    msg = conn.recv(msg_len).decode()
                    if msg == DISCONNECT_MESSAGE:
                        connected = False
                        print(f"[DISCONNECT] {addr} disconnected.")
                        break
                    print(f"[{addr}] {msg}")
                    conn.send("Msg received".encode())
                else:
                    connected = False
            except Exception as e:
                print(f"[ERROR] {e}")
                connected = False
                
        conn.close()
    
    def create_handle_client_thread(self, conn, addr) -> threading.Thread:
        handle_client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
        handle_client_thread.daemon = True  # Make thread daemon so it exits when main thread exits
        handle_client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        return handle_client_thread
    
    def start(self):
        self.server.listen()
        print(f"[LISTENING] server is listening on {ADRR[0]}:{ADRR[1]}")
        try:
            while self.running:
                try:
                    conn, addr = self.server.accept()
                    self.create_handle_client_thread(conn, addr)
                except socket.error:
                    # If server socket was closed
                    break
        except Exception as e:
            print(f"[ERROR] {e}")
    
    def close(self):
        self.running = False
        self.server.close()
        print("[CLOSING] server closed.")
        
if __name__ == '__main__':
    server = Server()
    start_server_thread = threading.Thread(target=server.start)
    start_server_thread.daemon = True  # Make thread daemon so it exits when main thread exits
    start_server_thread.start()
    
    print("[SERVER] Press Ctrl+C to exit")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Shutting down server...")
        server.close()
        sys.exit(0)