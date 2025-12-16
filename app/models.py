# request-service/app/models.py
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

# 曲リクエストテーブルの定義
class DjRequest(Base):
    __tablename__ = "dj_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist = Column(String, index=True, nullable=False)
    requester_name = Column(String, nullable=False)
    is_played = Column(Boolean, default=False)
