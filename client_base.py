import socket
from typing import Optional

from const import IP, PORT, ADDR, FORMAT, SIZE, DISCONNECT_MSG


class Client:
    @staticmethod
    def send_request(msg) -> Optional[str]:
        """
        Sends a request message to the server and returns the received message.

        Args:
            msg (str): The message to be sent to the server.

        Returns:
            str: The received message from the server, or None if the message is a disconnect message.
        """
        rcv_msg: Optional[str] = None
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        if msg != DISCONNECT_MSG:
            client.send(msg.encode(FORMAT))
            rcv_msg = client.recv(SIZE).decode(FORMAT)
        client.close()
        return rcv_msg

    @staticmethod
    def shutdown_server() -> None:
        """
        Sends a shutdown message to the server to gracefully terminate the connection.
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        client.send(DISCONNECT_MSG.encode(FORMAT))
        client.close()



def main() -> None:
    while True:
        msg = input("> ")

        try:
            if msg == DISCONNECT_MSG:
                print(f"[DISCONNECTED] Client disconnected from server at {IP}:{PORT}")
                try:
                    Client.shutdown_server()
                except Exception as e:
                    print(f"[CLIENT] server already disconnected")
                break
            else:
                if recv_msg := Client.send_request(msg):
                    print(f"[SERVER] to [CLIENT] {recv_msg}")
        
        except Exception as e:
            print(f"[CLIENT] failed to send request {msg} - [Error] {e}")
            break

if __name__ == "__main__":
    main()