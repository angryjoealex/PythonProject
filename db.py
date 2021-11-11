import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(f'postgresql://{settings.SQL_LOGIN}:{settings.SQL_PASSWORD}@127.0.0.1:5432/apetrov')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()