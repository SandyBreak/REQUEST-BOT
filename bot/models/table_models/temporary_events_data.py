# -*- coding: UTF-8 -*-

from sqlalchemy import Column, String, Integer, BigInteger

from .base import Base


class TemporaryEventsData(Base):
    __tablename__ = 'temporary_events_data'
    
    id = Column(Integer, primary_key=True)
    
    id_tg = Column(BigInteger, nullable=False)
    type_event = Column(String(length=128), nullable=False) 

    info = Column(String(length=2048), nullable=True)
    phone = Column(String(length=4096), nullable=True)