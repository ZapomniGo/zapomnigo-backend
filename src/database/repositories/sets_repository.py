from typing import List, Tuple

from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from sqlalchemy import desc, asc, func

from src.database.models import Organizations, Categories, OrganizationsUsers, Users, FoldersSets
from src.database.models.base import db
from src.database.models.sets import Sets


class SetsRepository:

    @classmethod
    def get_organization_sets(cls, organization_id: str) -> List[Sets] | None:
        return db.session.query(Sets).filter_by(organization_id=organization_id).all()

    @classmethod
    def get_set_by_id(cls, set_id: str) -> Sets | None:
        return db.session.query(Sets).filter_by(set_id=set_id).first()

    @classmethod
    def _base_query(cls) -> Query:
        """"
        SELECT sets.set_id, sets.set_name, sets.set_description, sets.set_modification_date, c.category_name,
        o.organization_name, f.flashcard_id, f.term, f.definition, f.notes
        FROM sets
            left join public.categories c on c.category_id = sets.set_category
            inner join public.users u on u.user_id = sets.user_id
            left join public.organizations_users ou on u.user_id = ou.user_id
            left join public.organizations o on o.organization_id = ou.organization_id
        """
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
    def _sets_in_folder_query(cls, folder_id):
        return cls._base_query().join(FoldersSets, FoldersSets.set_id == Sets.set_id).filter(
            FoldersSets.folder_id == folder_id)

    @classmethod
    def get_all_sets(
            cls,
            page: int = 1,
            size: int = 20,
            category_id: str = "",
            user_id: str = "",
            folder_id: str = "",
            sort_by_date: bool = True,
            ascending: bool = False,
    ) -> Pagination:
        """
        Retrieve a paginated list of sets from the database based on passed params for filtering and sorting

        Args:
            page (int): The page number to retrieve (default is 1).
            size (int): The number of sets per page (default is 20).
            category_id (str) If passed shows all sets with the given category
            user_id (str): If provided, fetch sets associated with the specified user (default is an empty string).
            folder_id (str): If provided, fetch sets in the given folder (default is an empty string).
            sort_by_date (bool): If True (default), the sets are ordered by creation date.
            ascending (bool): If True, the sets are ordered in ascending order, else in descending order.

        Returns:
            Pagination: A paginated result containing sets based on the specified parameters.
        """

        query = cls._base_query()

        if category_id:
            query = query.filter(Categories.category_id == category_id)

        if user_id:
            query = query.filter(Users.user_id == user_id)

        if folder_id:
            query = cls._sets_in_folder_query(folder_id)

        if sort_by_date:
            order_by_clause = desc(func.substring(Sets.set_id, 1, 10)) if not ascending else asc(
                func.substring(Sets.set_id, 1, 10))
        else:
            order_by_clause = asc(Sets.set_name) if ascending else desc(Sets.set_name)

        pagination: Pagination = query.order_by(order_by_clause).paginate(page=page, per_page=size, error_out=True)

        return pagination
