"""
    分发任务以及数据库更新
"""


from queue import Queue
from threading import Thread
from database import engine, Person
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(engine)
session = Session()


class TaskManager:
    # 利用 FIFO 队列作为任务队列
    task_queue = Queue()

    def __init__(self):
        # 把分数为0的人加入任务队列
        person_list = session.query(Person).filter(Person.score == 0).all()
        for person in person_list:
            self.add_task(Task(person))

    def add_task(self, task):
        """ 添加任务方法 """
        self.task_queue.put(task)

    def get_task(self):
        """ 获取任务 """
        return self.task_queue.get()


class UpdateSession:
    """ 专门更新数据库 """
    update_queue = Queue()

    def add_update(self, person_id, score):
        self.update_queue.put((person_id, score))

    def get_update(self):
        return self.update_queue.get()

    def update(self):
        sess_update = Session()                  # 与查询 session 分离
        while True:
            if self.update_queue.empty():        # 无任务的情况
                continue

            person_id, score = self.get_update()
            print('Updating {0} score: {1}'.format(person_id, score))

            person = sess_update.query(Person).filter_by(id=person_id).first()
            person.score = score

            sess_update.add(person)
            sess_update.commit()

    def start_update(self):
        """ 使用一个线程一直查看 update_queue 中是否有任务 """
        Thread(target=self.update).start()


update_session = UpdateSession()
update_session.start_update()


class Task:
    def __init__(self, person):
        self.person_id = person.id
        self.person = person

    def update_score(self, score):
        # 将分数改变任务添加到更新队列中
        update_session.add_update(self.person_id, score)
