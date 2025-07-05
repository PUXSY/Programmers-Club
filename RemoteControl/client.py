import socket
import threading
from info import Global_Vribols
import sys
import time

GV = Global_Vribols()
ADRR = GV.ADRR()
DISCONNECT_MESSAGE = "DISCONNECT"

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADRR)
        self.running = True

    def send(self, msg: str):
        try:
            message = msg.encode()
            msg_len = len(message)
            send_len = str(msg_len).encode()
            send_len += b' ' * (1024 - len(send_len))
            self.client.send(send_len)
            self.client.send(message)
            
            response = self.client.recv(1024).decode()
            print(f"[SERVER] {response}")
        except Exception as e:
            print(f"[ERROR] {e}")
    
    def receive_messages(self):
        while self.running:
            try:
                response = self.client.recv(1024).decode()
                if response:
                    print(f"[SERVER] {response}")
            except:
                # Connection closed or error
                self.running = False
                break
    
    def disconnect(self):
        print("[DISCONNECTING] Closing connection to server...")
        if self.running:
            self.send(DISCONNECT_MESSAGE)
            self.running = False
            self.client.close()
            sys.exit(0)

if __name__ == "__main__":
    client = Client()
    
    # Start a thread to receive messages
    receive_thread = threading.Thread(target=client.receive_messages)
    receive_thread.daemon = True
    receive_thread.start()
    
    print("Type your messages below (type 'exit' to disconnect):")
    try:
        while client.running:
            message = input()
            if message.lower() == 'exit':
                client.disconnect()
                time.sleep(0.1)
                break
            else:
                client.send(message)
                time.sleep(0.1)
                continue
    except KeyboardInterrupt:
        client.disconnect()
        sys.exit(0)