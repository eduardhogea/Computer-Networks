import sys, socket
import echo_util
from datetime import *

HOST = '127.0.0.1'
PORT = echo_util.PORT


group = []
group.append(date.today)
date_client=str(group[0])

#date_client="11-11-2020"


ok="OK"


if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))  #connect to server
    except ConnectionError:
        print('Socket error on connection')
        sys.exit(1)

    print('\nConnected to {}:{}'.format(HOST, PORT))

    try:
        date_server = echo_util.recv_msg(sock)
        print("Received Date")
        echo_util.send_msg(sock, date_client)
        if date_server==date_client:
            print("Dates match")
            echo_util.send_msg(sock, ok)

        else:
            print("Dates do not match")

    except ConnectionError:
        print('Socket error during communication')
        sock.close()
        print('Closed connection to server\n')

    print("Closing connection")
    sock.close()