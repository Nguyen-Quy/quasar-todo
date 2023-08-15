from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# engine = create_engine("sqlite:///todo.db")
engine = create_engine("mysql+pymysql://quynd:quy1234@mysql/quasar_todo")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    done = Column(Boolean, default=False)


Base.metadata.create_all(engine)
