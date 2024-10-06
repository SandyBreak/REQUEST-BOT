# -*- coding: UTF-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, BOOLEAN
from sqlalchemy.orm import relationship

from .base import Base


class CreatedEvent(Base):
    __tablename__ = 'created_events'
    
    id = Column(Integer, primary_key=True, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="created_event")

    date_creation = Column(TIMESTAMP, nullable=False) 
    type_event = Column(String(length=128), nullable=False) 
    info = Column(String(length=2048), nullable=False)
    phone = Column(String(length=4096), nullable=True)
