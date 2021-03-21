from core.database import Base
from sqlalchemy import Column, String, Integer


class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True)
    identifier = Column(String, unique=True)
    name = Column(String)
    channel = Column(String)
    server = Column(String)
