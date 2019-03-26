# -*- coding: utf-8 -*-


import settings
from socket import socket, AF_INET, SOCK_STREAM


class Client:
    # 连接 Commander
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((settings.COMMANDER_IP, settings.COMMANDER_PORT))

    def __init__(self):
        pass

    def report(self, massage):
        """ 回传信息给服务器 """
        self.s.send(massage)

    def deal(self):
        """ 处理指挥官命令 """
        pass

    def start(self):
        """ 开始任务 """
        pass
