from abc import ABC

from app.modules.users.models import UserModel
from app.modules.users.schemas.user import UserCreate, UserUpdate
from app.shared.interfaces.repositories import IPostgresBaseRepo


class IUserRepo(IPostgresBaseRepo[UserModel, UserCreate, UserUpdate], ABC):
    pass
