from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.modules.users.filters.user import UserFilter
from app.modules.users.models import UserModel
from app.modules.users.schemas.user import UserCreate, UserUpdate
from app.shared.interfaces.repositories import IPostgresBaseRepo
from app.shared.schemas import CursorPaginationParams, PaginationParams
from app.shared.schemas.sort import SortParams


class IUserRepo(IPostgresBaseRepo[UserModel, UserCreate, UserUpdate], ABC):
    """
    Interface for the user repository in PostgreSQL.

    Defines user-specific read operations on top of the generic PostgreSQL
    CRUD repository contract.
    """

    @abstractmethod
    async def get_paginated_users(
        self,
        pagination_params: PaginationParams,
        filters: UserFilter,
        sort_params: SortParams,
    ) -> tuple[Sequence[UserModel], int]:
        """
        Get users using offset pagination, filters, and sorting.

        :param pagination_params: Limit and offset pagination settings.
        :param filters: SQL filter object with user filter values.
        :param sort_params: Sort field and direction.
        :return: Sequence of user models and total number of matching records.
        """
        ...

    @abstractmethod
    async def get_cursor_paginated_users(
        self,
        pagination_params: CursorPaginationParams,
        filters: UserFilter,
        sort_params: SortParams,
    ) -> tuple[Sequence[UserModel], int]:
        """
        Get users using cursor pagination, filters, and sorting.

        :param pagination_params: Cursor, direction, and page size settings.
        :param filters: SQL filter object with user filter values.
        :param sort_params: Sort field and direction.
        :return: Sequence of user models and total number of matching records
            after cursor filtering.
        """
        ...
