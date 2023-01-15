# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from .utils import SaveMixin

Base = declarative_base()
metadata = Base.metadata


# in more complex projects, I prefer to use custom classes based on Base
class Statistic(Base, SaveMixin):
    __tablename__ = 'statistics'

    id = Column(INTEGER(11), primary_key=True)
    date = Column(Date, nullable=False, comment='event date')
    views = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='views num')
    clicks = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='clicks num')
    cost = Column(DECIMAL(19, 2), nullable=False, server_default=text("0.00"), comment='click cost')

    __addition_params = ['cpm', 'cpc']

    @classmethod
    def get_model_columns(cls, add_addition=False):
        columns = [column.name for column in Statistic.__table__.columns]
        if add_addition:
            columns += cls.__addition_params

        return columns
