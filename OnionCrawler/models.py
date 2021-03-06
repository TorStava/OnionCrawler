from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import datetime
import settings


DeclarativeBase = declarative_base()


def db_connect():

    return create_engine(URL(**settings.DATABASE))


def create_memex_table(engine):
    
    DeclarativeBase.metadata.create_all(engine)


class CrawlerData(DeclarativeBase):
    __tablename__ = "memex" + str(datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S"))

    id = Column(Integer, primary_key=True)
    utctimestamp = Column('utctimestamp', DateTime, nullable=True)
    url = Column('url', String, nullable=True)
    #title = Column('title', String, nullable=True)
    body = Column('body', String, nullable=True)