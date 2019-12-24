from sqlalchemy import Column, Integer, String, DateTime, \
    Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

COLUMN_WIDTH = 25
db_str = 'postgres://anton:password@localhost:5432/labs'
db = create_engine(db_str)
Base = declarative_base()


class MyBase:
    def __init__(self, **kwargs):
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __clean_dict(self):
        clean = self.__dict__.copy()
        clean.pop('_sa_instance_state')
        return clean

    def get_columns(self):
        return self.__clean_dict().keys()

    def get_values(self):
        return self.__clean_dict().values()


class User(MyBase, Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    user_age = Column(Integer)

    questions = relationship('Question')
    answers = relationship('Answer')


class Question(MyBase, Base):
    __tablename__ = 'question'

    question_id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False)
    question_datetime = Column(DateTime)
    question_user_id = Column(Integer, ForeignKey('user.user_id'))

    answers = relationship('Answer')


class Answer(MyBase, Base):
    __tablename__ = 'answer'

    answer_id = Column(Integer, primary_key=True)
    answer_text = Column(String, nullable=False)
    answer_is_valid = Column(Boolean, default=False)
    answer_user_id = Column(Integer, ForeignKey('user.user_id'))
    answer_question_id = Column(Integer, ForeignKey('question.question_id'))


session = sessionmaker(db)()
Base.metadata.create_all(db)

TABLES = {
    'user': ('user_id', 'user_name', 'user_age'),
    'question': ('question_id', 'question_text', 'question_datetime', 'question_user_id'),
    'answer': ('answer_id', 'answer_text', 'answer_is_valid', 'answer_user_id', 'answer_question_id')
}

MODELS = {'user': User, 'question': Question, 'answer': Answer}


def insert(table, opts):
    object_class = MODELS[table]
    obj = object_class(**opts)
    session.add(obj)


def get(table, opts=None):
    objects_class = MODELS[table]
    objects = session.query(objects_class)
    for key, item in opts.items():
        objects = objects.filter(getattr(objects_class, key) == item)

    return list(objects)


def update(table, condition, opts):
    column, value = condition
    object_class = MODELS[table]
    filter_attr = getattr(object_class, column)
    objects = session.query(object_class).filter(filter_attr == value)

    for obj in objects:
        for key, item in opts.items():
            setattr(obj, key, item)


def delete(table, opts):
    objects_class = MODELS[table]
    objects = session.query(objects_class)
    for key, item in opts.items():
        objects = objects.filter(getattr(objects_class, key) == item)

    objects.delete()


def commit():
    session.commit()
