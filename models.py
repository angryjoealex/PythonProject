from sqlalchemy import Column, Integer, String, Boolean
from db import Base, engine


class job(Base):
    __tablename__ = 'mail2ftp'
    id = Column(String, primary_key=True)
    postfix_id = Column(String)
    transport = Column(String)
    host = Column(String)
    login = Column(String)
    password = Column(String)
    port = Column(String)
    remote_dir = Column(String)
    key = Column(String)
    file = Column(String)
    local = Column(Boolean)
    last_error = Column(String)
    status = Column(String)
    last_status_ts = Column(String)
    attempts = Column(Integer)
    next_attempt = Column(String)

    def __repr__(self):
        return f'<job {self.id} {self.postfix_id}>'
