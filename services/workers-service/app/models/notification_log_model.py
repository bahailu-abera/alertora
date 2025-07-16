import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON
from app.extensions import Base


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    notification_type = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    content = Column(JSON, nullable=False)
    status = Column(String, nullable=False)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
