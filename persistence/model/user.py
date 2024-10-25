from alchemical import Model
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

roles = {
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

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def set_role(self, role_name):
        if role_name not in roles.keys():
            raise ValueError(f'Role {role_name} is not allowed')
        self.role = role_name
        self.save()

    @property
    def role_hun(self):
        return roles[self.role]


from persistence.repository.user import UserRepository
