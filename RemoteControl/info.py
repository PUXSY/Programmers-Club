import socket
class Global_Vribols:
    def __init__(self) -> None:
        self._HOST_IP: str = socket.gethostbyname(socket.gethostname())
        self._PORT: int = 1237
        
    def get_host_ip(self) -> str:
        return self._HOST_IP
    
    def get_port(self) -> int :
        return self._PORT
    
    def ADRR(self):
        return (self.get_host_ip(), self.get_port())
    