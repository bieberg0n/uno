import socket
import json


def main():
    s = socket.socket()
    s.connect(('127.0.0.1', 9900))
    # s2 = socket.socket()
    # s2.connect(('127.0.0.1', 9900))

    msg = dict(
        action='join',
        )
    s.sendall(json.dumps(msg).encode())
    # s2.sendall(json.dumps(msg).encode())

    data_str = s.recv(512).decode()
    data = json.loads(data_str)

    # data2_str = s2.recv(512).decode()
    # data2 = json.loads(data2_str)

    msg = dict(
        action='ready',
        id=data['id']
        )
    s.sendall(json.dumps(msg).encode())
    # print(s.recv(512))

    # msg = dict(
    #     action='ready',
    #     id=data2['id']
    #     )
    # s2.sendall(json.dumps(msg).encode())
    print(s.recv(512))
    # print(s2.recv(512)


main()
