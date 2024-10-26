from alchemical import Model
from flask import g
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, validates
from werkzeug.security import check_password_hash, generate_password_hash


# Maximum 64 characters
roles = {
    'super_admin': 'Főadminisztrátor',
    'admin': 'Adminisztrátor',
    'user': 'Felhasználó',
}


class User(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(180), nullable=False)
    role: Mapped[str] = mapped_column(String(64), nullable=False)

    def save(self):
        UserRepository.save(self)

    def delete(self):
        UserRepository.delete(self)

    @property
    # Determines whether the user is the original admin
    def is_super_admin(self):
        return self.role == 'super_admin'

    @property
    def is_admin(self):
        return self.role in ["admin", "super_admin"]

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def set_role(self, role_name):
        if role_name not in roles.keys() or role_name == 'super_admin':
            raise ValueError(f'Role {role_name} is not allowed')
        self.role = role_name

    @property
    def role_hun(self):
        return roles[self.role]

    def form_update(self, form):
        self.name = form.name.data
        self.set_role("user")
        self.set_password(form.password.data)


from persistence.repository.user import UserRepository
