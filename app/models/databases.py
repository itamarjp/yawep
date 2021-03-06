import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))


#engine = create_engine('sqlite:///' + os.path.join(basedir, 'storage.db'), convert_unicode=True)

#engine = create_engine('postgresql+psycopg2://postgres:password@localhost/webpanel'), convert_unicode=True)
engine = create_engine('postgresql+pg8000://postgres:password@localhost/webpanel'), convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  # import all modules here that might define models so that
  # they will be registered properly on the metadata. Otherwise
  # you will have to import them first before calling init_db()
  import app.models
  Base.metadata.create_all(bind=engine)
