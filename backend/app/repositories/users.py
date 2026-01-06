from sqlalchemy.orm import Session

from ..models import User, UserRole
from ..security import get_password_hash


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str, full_name: str, role: UserRole, org_id: str | None = None) -> User:
    user = User(email=email, password_hash=get_password_hash(password), full_name=full_name, role=role, org_id=org_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
