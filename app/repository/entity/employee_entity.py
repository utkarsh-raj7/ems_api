from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.common.constant.role import Role

class Base(DeclarativeBase):
    pass

class EmployeeEntity(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    department: Mapped[str] = mapped_column(String(50), nullable=True, default=None)
    role: Mapped[str] = mapped_column(String(100), nullable=True, default=Role.STAFF)
    password_hash: Mapped[str] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    created_by: Mapped[str | None] = mapped_column(String(100))
    modified_by: Mapped[str | None] = mapped_column(String(100))