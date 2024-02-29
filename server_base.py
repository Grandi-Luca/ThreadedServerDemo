import random
import socket
import threading
import time

from const import IP, PORT, ADDR, FORMAT, SIZE, DISCONNECT_MSG, INIT_MSG, SERVER_MAX_TIMEOUT, SERVER_TIMEOUT_WITHOUT_CLIENT, SERVER_INIT_MSG, SERVER_NOT_READY_MSG

ending_connection = False

def handle_func(conn: socket.socket, addr: tuple, msg: str) -> None:
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
    

def handle_client_separatelly(conn: socket.socket, addr: tuple, msg: str) -> None:
    """
    Handles the client's request in a separate thread.

    Args:
        server (Server): The server object.
        conn (socket): The client's socket connection.
        addr (tuple): The client's address.
        msg (str): The client's message.

    Returns:
        None
    """
    thread: threading.Thread = threading.Thread(target=handle_func, args=(conn, addr, msg))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def main() -> None:
    """
    Entry point of the server application.
    """
    print("[STARTING] Server is starting...")
    server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    server_init: bool = False
    server.settimeout(SERVER_TIMEOUT_WITHOUT_CLIENT)

    # init server
    while not server_init:
        conn, addr = server.accept()
        recv_msg: str = conn.recv(SIZE).decode(FORMAT)

        if recv_msg == INIT_MSG:
            print(f"[{addr}] initialization {recv_msg}")

            # Simulate some processing time
            time.sleep(random.randint(3, 10))
            server_init = True
            conn.send(SERVER_INIT_MSG.encode(FORMAT))
            break
        
        if not server_init:
            conn.send(SERVER_NOT_READY_MSG.encode(FORMAT))

        # reset timeout
        server.settimeout(SERVER_MAX_TIMEOUT)
        conn.close()

    
    print("[SERVER INITIALIZED] Server is ready to receive requests")

    # handle clients request
    while True:
        conn, addr = server.accept()
        recv_msg: str = conn.recv(SIZE).decode(FORMAT)

        if recv_msg == DISCONNECT_MSG:
            print("[ENDING] Ending server connection")
            break


        # handle client's request in a separate thread
        handle_client_separatelly(conn, addr, recv_msg)
        # reset timeout
        server.settimeout(SERVER_MAX_TIMEOUT)

    server.close()


if __name__ == "__main__":
    try:
        main()
    except socket.timeout:
        pass