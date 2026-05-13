# repository/entity/employee_entity.py
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# In SQLAlchemy 2.0, we use a class for the Base instead of a function
class Base(DeclarativeBase):
    pass

class EmployeeEntity(Base):
    __tablename__ = "employee"

    # 1. Primary Key (always first)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[String] = mapped_column()
    last_name: Mapped[String] = mapped_column()
    email: Mapped[String(100)]] = mapped_column()
    department: Mapped[String] = mapped_column()
    role: Mapped[String | None = "staff"] = mapped_column()
    password_hash: Mapped[String] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    created_by: Mapped[String] = mapped_column()
    modified_by: Mapped[String] = mapped_column()
    
    # 4. Audit Columns (Who)
    # Your turn: Add `created_by` and `modified_by`. 
    # Make them optional strings (since a system might create the first admin user, not a person).
    
    # [YOUR CODE HERE]