from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


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
    name = Column(String)
    leader = Column(String)  # 순장
    cell_group = Column(String)  # 다락방/소그룹
    content = Column(String)
    created_at = Column(DateTime)
    is_private = Column(Boolean, default=False)  # 비공개 여부
