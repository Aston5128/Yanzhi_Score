import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


sql_link = 'mysql+pymysql://root:********#@127.0.0.1/face_score?charset=utf8'
engine = create_engine(sql_link)
base = declarative_base()


class Person(base):

    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    school = db.Column(db.String(60))
    person_class = db.Column(db.String(75))
    person_image = db.Column(db.String(256), unique=True)
    score = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return '<Person {0}>'.format(self.id)


if __name__ == '__main__':
    base.metadata.create_all(engine)
