from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from db import Base, engine


class Job(Base):
    __tablename__ = 'mail2ftp'
    idx = Column(BigInteger, primary_key=True, autoincrement=True)
    id = Column(String)
    added = Column(BigInteger)
    postfix_id = Column(String)
    transport = Column(String)
    host = Column(String)
    login = Column(String)
    password = Column(String)
    port = Column(Integer)
    folder = Column(String)
    key = Column(String)
    file = Column(String)
    filetitle = Column(String)
    spool = Column(String)
    options = Column(String)
    new_filename = Column(String)
    local = Column(Boolean)
    last_error = Column(String)
    status = Column(String)
    last_status_ts = Column(BigInteger)
    attempts = Column(Integer)
    next_attempt = Column(String)
    failyre_reply = Column(String)
    succes_reply = Column(String)

    def __repr__(self):
        return f'<job {self.id} {self.postfix_id}>'
