from typing import List, Optional
from typing import Optional

def create_user_in_db(session: Session, user_data: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos."""
    db_user = User.model_validate(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Obtiene un usuario por su nombre de usuario."""
    return session.exec(select(User).where(User.username == username)).first()

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """Obtiene un usuario por su ID."""
    return session.exec(select(User).where(User.id == user_id)).first()
