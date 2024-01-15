from datetime import datetime
from typing import Dict, Any, List, Tuple

from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from sqlalchemy import select, Row, desc, asc, func
from ulid import ULID

from src.database.models import Organizations, Categories, Flashcards, OrganizationsUsers, Users
from src.database.models.base import db
from src.database.models.sets import Sets
from src.database.repositories.users_repository import UsersRepository


class SetsRepository:

    @classmethod
    def get_creator_username(cls, user_id: str) -> str:
        return str(UsersRepository.get_user_by_ulid(user_id).username)

    @classmethod
    def get_organization_sets(cls, organization_id: str) -> List[Sets] | None:
        return db.session.query(Sets).filter_by(organization_id=organization_id).all()

    @classmethod
    def get_set_by_id(cls, set_id: str) -> Sets | None:
        return db.session.query(Sets).filter_by(set_id=set_id).first()

    @classmethod
    def _base_query(cls) -> Query:
        return db.session.query(
            Sets.set_id, Sets.set_name, Sets.set_description, Sets.set_modification_date,
            Categories.category_name, Organizations.organization_name, Users.username
        ).outerjoin(Categories, Categories.category_id == Sets.set_category) \
            .join(Users, Users.user_id == Sets.user_id) \
            .outerjoin(OrganizationsUsers, Users.user_id == OrganizationsUsers.user_id) \
            .outerjoin(Organizations, Organizations.organization_id == OrganizationsUsers.organization_id)

    @classmethod
    def get_set_info(cls, set_id: str) -> List[Tuple[...]]:
        return cls._base_query().filter(Sets.set_id == set_id).all()

    @classmethod
    def get_all_sets(
            cls,
            page: int = 1,
            size: int = 20,
            user_id: str = "",
            sort_by_date: bool = True,
            ascending: bool = False,
    ) -> Pagination:
        """
        Retrieve a paginated list of sets from the database.

        Args:
            page (int): The page number to retrieve (default is 1).
            size (int): The number of sets per page (default is 20).
            user_id (str): If provided, fetch sets associated with the specified user (default is an empty string).
            sort_by_date (bool): If True (default), the sets are ordered by creation date.
            ascending (bool): If True, the sets are ordered in ascending order, else in descending order.

        Returns:
            Pagination: A paginated result containing sets based on the specified parameters.
        """

        query = cls._base_query()

        if user_id:
            query = query.filter(Users.user_id == user_id)

        if sort_by_date:
            order_by_clause = desc(func.substring(Sets.set_id, 1, 10)) if not ascending else asc(
                func.substring(Sets.set_id, 1, 10))
        else:
            order_by_clause = asc(Sets.set_name) if ascending else desc(Sets.set_name)

        pagination: Pagination = query.order_by(order_by_clause).paginate(page=page, per_page=size, error_out=True)

        return pagination

    @classmethod
    def edit_set(cls, set_obj: Sets, json_data: Dict[str, Any]) -> None:
        set_obj.set_name = json_data.get("set_name", set_obj.set_name)
        set_obj.set_description = json_data.get("set_description", set_obj.set_description)
        set_obj.set_modification_date = str(datetime.now())

        try:
            # Checks for falsify values like "" and None
            if not json_data["set_category"]:
                set_obj.set_category = None
            else:
                set_obj.set_category = json_data["set_category"]
        except KeyError:
            set_obj.set_category = set_obj.set_category

        db.session.commit()
