from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class DepartmentEnum(str, enum.Enum):
    GROUND = "地面科"
    COMMAND = "指挥科"
    OPERATION = "作业科"
    OFFICE = "办公室"
    SUPPORT = "保障科"

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    department = Column(String, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    created_at = Column(DateTime, default=datetime.utcnow)

    contracts = relationship("Contract", back_populates="uploader")

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    department = Column(String, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    uploader_name = Column(String, nullable=False)
    party_a = Column(String, nullable=False)
    party_b = Column(String, nullable=False)
    signing_date = Column(DateTime, nullable=False)
    execution_start_date = Column(DateTime, nullable=False)
    execution_end_date = Column(DateTime, nullable=False)
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    uploader = relationship("User", back_populates="contracts")
