import sys, socket
import echo_util

HOST = '127.0.0.1'
PORT = 31337
secventa = sys.argv[-1] if len(sys.argv) > 1 else 0
temp=""

if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT)) 
    except ConnectionError:
        print('Socket error on connection')
        sys.exit(1)

    print('\nConnected to {}:{}'.format(HOST, PORT))

    try:
        echo_util.send_msg(sock, str(secventa))
        print('Sent request')
        temp = echo_util.recv_msg(sock)
        print("Assigned sequence: {} - {}".format(str(int(temp)-int(secventa)+1), temp))
    except ConnectionError:
        print('Socket error during communication')
        sock.close()
        print('Closed connection to server\n')
        

    print("Closing connection")
    sock.close()