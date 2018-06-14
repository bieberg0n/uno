import socket
import json


def log(*args):
    print(*args)


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

    print(data)
    print(s.recv(512))
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
    resp = json.loads(s.recv(512).decode())
    log(resp)
    cards = resp['cards']

    msg = dict(
        action='push',
        id=data['id'],
        cards=[cards[0]]
        # cards=['y9']
    )
    s.sendall(json.dumps(msg).encode())
    print(json.loads(s.recv(512).decode()))


main()
