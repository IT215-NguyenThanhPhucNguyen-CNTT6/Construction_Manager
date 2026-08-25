from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class ConstructionSite(Base):
    __tablename__ = "construction_sites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    address = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    # Khóa ngoại 1-N: Lưu người tạo/chủ nhiệm công trường
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # mqh
    creator = relationship("User", back_populates="created_sites")
    members = relationship("SiteMember", back_populates="site", cascade="all, delete-orphan")
    work_items = relationship("WorkItem", back_populates="site", cascade="all, delete-orphan")


class SiteMember(Base):
    __tablename__ = "site_members"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("construction_sites.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), default="MEMBER")  # MANAGER, SUPERVISOR, MEMBER
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # mqh
    site = relationship("ConstructionSite", back_populates="members")
    user = relationship("User", back_populates="memberships")
