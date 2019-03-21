from score import Score
from socket import socket, AF_INET, SOCK_STREAM


s = socket(AF_INET, SOCK_STREAM)
s.connect(('192.168.1.31', 13140))
score = Score()


if __name__ == '__main__':
    while True:
        s.send(b'start')
        # 图片接收
        person_image = b''
        while True:
            recv = s.recv(1024)
            if recv.endswith(b'image_stream_end'):
                recv = recv.replace(b'image_stream_end', b'')
                person_image += recv
                break
            person_image += recv

        s.send(bytes('score: {0}'
                     ''.format(score.score(person_image)).encode('utf-8')))
