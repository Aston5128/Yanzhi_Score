#! /usr/bin/env python
# -*- coding:utf-8 -*-


from score import Score
from client import Client


class SoldierClient(Client):
    # 预先实例 score 对象，防止重复建立，节省资源
    score = Score()

    def deal(self):
        # 告诉服务端新的一轮可以开始
        self.report(b'start')

        # 图片接收
        person_image = b''
        while True:
            recv = self.s.recv(1024)
            if recv.endswith(b'image_stream_end'):
                recv = recv.replace(b'image_stream_end', b'')
                person_image += recv
                break
            person_image += recv

        # 获取分数，并发送给服务端
        score_text = self.score.score(person_image)
        self.report(bytes('score: {0}'.format(score_text).encode('utf-8')))

    def start(self):
        while True:
            recv_done = self.s.recv(1024)

            # 只有在接收到服务器返回的 done 字段才会开始
            if recv_done == b'done':
                self.deal()


if __name__ == '__main__':
    SoldierClient().start()
