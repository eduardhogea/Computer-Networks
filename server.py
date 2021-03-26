import echo_util
import threading
import sys

HOST = '0.0.0.0'
PORT = 31337
list=[0]

secv = int(sys.argv[-1] if len(sys.argv) > 1 else 0)
list[0]=secv

def handle_client(sock, addr):
    """ Receive data from the client via sock and echo it back """
    try:
        msg = echo_util.recv_msg(sock) # Blocks until received
        # complete message
        print("Received request for seq lengt " + msg)
        nsecv = int(msg)

        response = str(list[0]+nsecv - 1)
        list[0] += nsecv

        echo_util.send_msg(sock, response) # Blocks until sent
    except:
        sock.close()
    print('Closed connection...')



if __name__ == '__main__':
    listen_sock = echo_util.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))
    connected = True
    while connected:
        client_sock, addr = listen_sock.accept()
        # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
        thread = threading.Thread(target = handle_client, args = [client_sock, addr], daemon=True)
        thread.start()
        print('Accept client {}'.format(addr))