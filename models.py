from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base
import os


class CellGroup(Base):
    __tablename__ = "cell_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # 다락방 이름 (예: 은혜다락방)
    leaders = relationship("Leader", back_populates="cell_group")


class Leader(Base):
    __tablename__ = "leaders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # 순장 이름
    cell_group_id = Column(Integer, ForeignKey("cell_groups.id"))
    cell_group = relationship("CellGroup", back_populates="leaders")


class Prayer(Base):
    __tablename__ = "prayers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)  # 이름 - 인덱스 추가
    leader = Column(String(100), nullable=False, index=True)  # 순장 - 인덱스 추가
    cell_group = Column(String(100), nullable=False, index=True)  # 다락방/소그룹 - 인덱스 추가
    content = Column(Text, nullable=False)  # 긴 텍스트를 위해 Text 타입 사용
    created_at = Column(DateTime(timezone=True), nullable=False, index=True)  # 타임존 지원, 인덱스 추가
    is_private = Column(Boolean, default=False, nullable=False, index=True)  # 비공개 여부 - 인덱스 추가
