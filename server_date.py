import echo_util
import threading
from datetime import *

HOST = echo_util.HOST
PORT = echo_util.PORT
group = []
group.append(date.today)
date_server=str(group[0])

def handle_client(sock, addr):
    """ Receive data from the client via sock and echo it back """
    while True:
        try:
            echo_util.send_msg(sock, str(date_server))
            date_client = echo_util.recv_msg(sock)
            print("Sent date")
            if date_client!=date_server:
                print('Received: {}'.format(date_client))
            else:
                ok=echo_util.recv_msg(sock)
                print("Received: {}".format(ok))

        except (ConnectionError, BrokenPipeError):
            print('Closed connection ...')
            sock.close()
            break


if __name__ == '__main__':
    listen_sock = echo_util.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))

    while True:
        client_sock, addr = listen_sock.accept()
        # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
        thread = threading.Thread(target = handle_client, args = [client_sock, addr], daemon=True)
        thread.start()
        print('Accept client {}'.format(addr))