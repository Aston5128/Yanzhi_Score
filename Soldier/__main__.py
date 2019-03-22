#! /usr/bin/env python
# -*- coding:utf-8 -*-


import time
from score import Score
from socket import socket, AF_INET, SOCK_STREAM


# 连接 Commander
s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 13140))

# 预先实例 score 对象，防止重复建立，节省资源
score = Score()


if __name__ == '__main__':
    while True:
        # 告诉服务端新的一轮可以开始
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

        # 获取分数，并发送给服务端
        score_text = score.score(person_image)
        s.send(bytes('score: {0}'.format(score_text).encode('utf-8')))

        # 通信时，有可能分数和 start 标记同时到达，所以 start 延迟 0.05 秒发出
        time.sleep(0.05)
