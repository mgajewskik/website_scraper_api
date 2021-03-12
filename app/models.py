from sqlalchemy import Column, Integer, String, DateTime, Text

from .database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    url = Column(String)
    started_at = Column(DateTime)
    status = Column(String, default="pending")
    completed_at = Column(DateTime, default=None)
    text = Column(Text, default=None)
