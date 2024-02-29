import random
import socket
import threading
import time

from const import IP, PORT, ADDR, FORMAT, SIZE, DISCONNECT_MSG, INIT_MSG, SERVER_MAX_TIMEOUT, SERVER_TIMEOUT_WITHOUT_CLIENT, SERVER_INIT_MSG, SERVER_NOT_READY_MSG

class Server():
    def __init__(self):
        """
        Initializes the server object.

        The server object is responsible for creating and managing the server socket.
        It binds the socket to the specified address and starts listening for incoming connections.
        The server is initially set to not initialized and has a timeout value set for clients.

        Args:
            None

        Returns:
            None
        """
        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.server.listen()
        self.server_init: bool = False
        self.server.settimeout(SERVER_TIMEOUT_WITHOUT_CLIENT)
    
    def _init_server(self) -> None:
        """
        Initialize the server.

        Args:
            None

        Returns:
            None
        """
        while not self.server_init:
            conn, addr = self.server.accept()
            recv_msg: str = conn.recv(SIZE).decode(FORMAT)

            if recv_msg == INIT_MSG:
                print(f"[{addr}] initialization {recv_msg}")

                # Simulate some processing time
                time.sleep(random.randint(3, 10))
                self.server_init = True
                conn.send(SERVER_INIT_MSG.encode(FORMAT))
                break
            
            if not self.server_init:
                conn.send(SERVER_NOT_READY_MSG.encode(FORMAT))

            # reset timeout
            self.server.settimeout(SERVER_MAX_TIMEOUT)
            conn.close()

    def _handle_client_separatelly(self, conn: socket.socket, addr: tuple, msg: str) -> None:
        """
        Handles the client's request in a separate thread.

        Args:
            conn (socket): The client's socket connection.
            addr (tuple): The client's address.
            msg (str): The client's message.

        Returns:
            None
        """
        thread: threading.Thread = threading.Thread(target=self._handle_func, args=(conn, addr, msg))
        thread.start()

    def _handle_func(self, conn: socket.socket, addr: tuple, msg: str) -> None:
        """
        Handle the client connection and process the received message.

        Args:
            conn (socket.socket): The client socket connection.
            addr (tuple): The address of the client.
            msg (str): The message received from the client.

        Returns:
            None
        """
        print(f"[{addr}] {msg}")

        # Simulate some processing time
        time.sleep(random.randint(1, 4))
        
        msg: str = f"Msg received: {msg}"
        conn.send(msg.encode(FORMAT))
        conn.close()

    def run(self) -> None:
        """
        Run the server.

        Args:
            None

        Returns:
            None
        """
        print("[STARTING] Server is starting...")
        print(f"[LISTENING] Server is listening on {IP}:{PORT}")
        self._init_server()
        print("[SERVER INITIALIZED] Server is ready to receive requests")

        # handle clients request
        while True:
            conn, addr = self.server.accept()
            recv_msg: str = conn.recv(SIZE).decode(FORMAT)

            if recv_msg == DISCONNECT_MSG:
                print("[ENDING] Ending server connection")
                break

            # handle client's request in a separate thread
            self._handle_client_separatelly(conn, addr, recv_msg)
            # reset timeout
            self.server.settimeout(SERVER_MAX_TIMEOUT)

    def close(self) -> None:
        """
        Close the server connection.

        Args:
            None

        Returns:
            None
        """
        self.server.close()


if __name__ == "__main__":
    try:
        server: Server = Server()
        server.run()
        server.close()
    except socket.timeout:
        pass