import socket
import struct

HOST = '127.0.0.1'
PORT = 1337

header_len = struct.Struct('!I')


def create_listen_socket(host, port):
    """ Setup the sockets our server will receive connection
    requests on """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    sock.listen(15)
    return sock


def recv_all(sock, length):
    """ Receive length bytes from socket; blocking """
    data = bytearray()

    while length:
        recvd = sock.recv(length)
        if not recvd:
            raise ConnectionError()

        data = data + recvd
        length = length - len(recvd)

    return data


def recv_msg(sock):
    """ Wait for data to arrive on the socket, then parse
    messages into length + actual data """

    lungime = recv_all(sock, header_len.size)
    (lungime,) = header_len.unpack(lungime)

    msg = recv_all(sock, lungime)
    msg = msg.decode('utf-8')
    return msg


def prep_msg(msg):
    """ Prepare a string to be sent as a message """
    lungime = len(msg)
    actual_msg = header_len.pack(lungime)
    actual_msg += msg.encode('utf-8')
    return actual_msg


def send_msg(sock, msg):
    """ Send a string over a socket, preparing it first """
    data = prep_msg(msg)
    sock.sendall(data)
