from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

engine = create_engine("sqlite:///test.db", echo=True)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
