import random
import socket
from threading import Thread
import time
from typing import List

from client_base import Client
from const import IP, PORT, DISCONNECT_MSG, INIT_MSG, HELLO_MSG, USELESS_MSG

msgs = [INIT_MSG, HELLO_MSG, USELESS_MSG, DISCONNECT_MSG]


def main(i: int) -> None:
    """
    Main function for the client thread.

    Args:
        i (int): The client number.

    Returns:
        None
    """
    i: int = 0
    while True:
        # Randomly select a message to send to the server
        msg: str = random.choice(msgs)
        msg: str = INIT_MSG if i == 0 else HELLO_MSG

        try:
            if msg == DISCONNECT_MSG:
                print(f"[DISCONNECTED] Client {i} disconnected from server at {IP}:{PORT}")
                break
            else:
                if recv_msg := Client.send_request(msg):
                    print(f"[SERVER] to [CLIENT {i}] {recv_msg}")
                
                # Simulate some processing time
                time.sleep(random.randint(1, 4))
            
            i+=1
        
        except Exception as e:
            print(f"[CLIENT {i}] failed to send request {msg} - [Error] {e}")
            break


if __name__ == "__main__":
    # Start all threads
    threads: List[Thread] = []
    for n in range(3):
        t = Thread(target=main, args=((n,)))
        t.start()
        threads.append(t)

    # Wait all threads to finish
    for t in threads:
        t.join()
    
    # Shutdown the server
    Client.shutdown_server()