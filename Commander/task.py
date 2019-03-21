"""
    分发任务
"""


from queue import Queue
from sqlalchemy.orm import sessionmaker
from database import engine, Person


Session = sessionmaker(engine)
session = Session()


class TaskManager:
    # 利用 FIFO 队列作为任务队列
    task_queue = Queue()

    def __init__(self):
        person_list = session.query(Person).filter(Person.score == 0).all()

        for person in person_list:
            self.add_task(Task(person))

    def add_task(self, task):
        self.task_queue.put(task)

    def get_task(self):
        return self.task_queue.get()


class Task:
    def __init__(self, person):
        self.person = person

    def update_score(self, score):
        temp_session = Session()
        self.person.score = score
        temp_session.add(self.person)
        temp_session.close()


if __name__ == '__main__':
    task_manager = TaskManager()
    print(task_manager.task_queue.qsize())
