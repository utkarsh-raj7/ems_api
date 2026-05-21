# init_db.py
from app.repository.database import engine, SessionLocal
from app.repository.entity.employee_entity import Base, EmployeeEntity
from app.common.constant.role import Role
from app.common.constant.department import Department
from app.common.security.security import get_password_hash


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tables created.")


def seed_admin(db) -> None:
    existing = db.query(EmployeeEntity).filter(EmployeeEntity.email == "admin@company.com").first()
    if existing:
        print("Super Admin already exists. Skipping.")
        return

    admin = EmployeeEntity(
        first_name="System",
        last_name="Admin",
        email="admin@company.com",
        phone="+910000000000",
        department=Department.ENGINEERING.value,
        role=Role.ADMIN.value,
        password_hash=get_password_hash("Admin@123!"),
        created_by=None,
        modified_by=None
    )
    db.add(admin)
    db.commit()
    print("Super Admin created. Login: admin@company.com / Admin@123!")


def run() -> None:
    create_tables()
    db = SessionLocal()
    try:
        seed_admin(db)
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()