from typing import Tuple
import socket

IP: str = socket.gethostbyname(socket.gethostname())
PORT: int = 8080
ADDR: Tuple[str, int] = (IP, PORT)
FORMAT: str = "utf-8"
SIZE: int = 1024
SERVER_MAX_TIMEOUT: int = 50
SERVER_TIMEOUT_WITHOUT_CLIENT: int = 100

DISCONNECT_MSG: str = "DISC"
INIT_MSG: str = "INIT"
HELLO_MSG: str = "HELLO"
USELESS_MSG: str = "USELESS"
SERVER_INIT_MSG: str = "Server initialized"
SERVER_NOT_READY_MSG: str = "Server is not ready"
