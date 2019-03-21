#! /usr/bin/env python3
# -*- coding:utf-8 -*-


from task import TaskManager
from server import EchoHandler, CommanderServer


task_manager = TaskManager()


class CommandHandler(EchoHandler):
    task = None

    def handle(self):
        print('Got connection from: ', self.client_address)

        while True:
            report = self.request.recv(1024)
            self.deal(report)

    def deal(self, report):
        """ 处理士兵报告 """
        if report == b'start':
            """士兵报告可以开始"""
            # 获取任务
            self.task = task_manager.get_task()

            # 读取图片，并发给士兵
            with open(self.task.person.person_image, 'rb') as file:
                self.wfile.write(file.read())

            # 图片发送完毕，发送截止字符串
            self.request.send(b'image_stream_end')
        elif report.startswith(b'score'):
            """士兵报告得分，并表示结束该任务，可以开始下一项任务"""
            score = float(report.strip(b'score: '))
            print('[{0} Task Done] {1} {2}'.format(self.client_address,
                                                   self.task.person.name,
                                                   score))
            self.task.update_score(score)


if __name__ == '__main__':
    CommanderServer(handler=CommandHandler).serve_forever()
