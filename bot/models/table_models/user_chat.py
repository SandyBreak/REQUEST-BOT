# -*- coding: UTF-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, BigInteger
from sqlalchemy.orm import relationship

from .base import Base


class UserChat(Base):
    __tablename__ = 'user_chats'
    
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="user_chats")
    
    id_topic_chat = Column(BigInteger, nullable=True)
