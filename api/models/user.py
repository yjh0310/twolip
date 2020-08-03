import hashlib
from datetime import datetime

from sqlalchemy import Column, orm
from sqlalchemy.dialects.mysql import CHAR, TEXT, DATETIME, BOOLEAN

from libs.database.types import Base

class UserState:

    def __init__(self, user):
        self.user = user

    def match(self):
        pass

class CoupleState(UserState):

    def match(self):
        print('?????')

class SingleState(UserState):

    def match(self):
        print('짝을 찾습니다.')


class User(Base):
    __tablename__ = 'users'
    phone = Column(CHAR(15), unique=True)
    password = Column(TEXT)
    nick_name = Column(CHAR(50), unique=True)
    picture = Column(TEXT)
    registered_at = Column(DATETIME, default=datetime.now())

    # profile
    religion = Column(TEXT)
    smoke = Column(BOOLEAN)
    job = Column(TEXT)
    school = Column(TEXT)
    major = Column(TEXT)
    company = Column(TEXT)
    is_couple = Column(BOOLEAN)

    def __init__(self, password, **kwargs):
        '''
        :param kwargs:
        '''
        super().__init__(**kwargs)
        self.phone = None
        self.password = self.gen_password_hash(password)

    @orm.reconstructor
    def init_on_load(self):
        if self.is_couple:
            self.state = CoupleState(self)
            return
        self.state = SingleState(self)

    @classmethod
    def gen_password_hash(cls, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def json(self):
        return {
            'id': self.id,
            'phone': self.phone,
            'nick_name': self.nick_name,
            'picture': self.picture,
            'religion': self.religion,
            'smoke': self.smoke,
            'job': self.job,
            'school': self.school,
            'major': self.major,
            'company': self.company,
        }


