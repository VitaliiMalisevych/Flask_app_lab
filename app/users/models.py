from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash

from app import db, bcrypt, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list['Post']] = relationship('Post', back_populates='author')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        if self.password.startswith(('$2a$', '$2b$', '$2y$')):
            return bcrypt.check_password_hash(self.password, password)
        if self.password.startswith(('scrypt:', 'pbkdf2:')):
            return check_password_hash(self.password, password)
        return False

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
