from typing import List, Tuple

from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from sqlalchemy import desc, asc, func, and_, case, or_
from sqlalchemy.orm import joinedload

from src.database.models import Categories, Users, FoldersSets, Subcategories, Flashcards
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
    def change_verified_status_set(cls, set_obj: Sets, verified: bool) -> None:
        set_obj.verified = verified
        db.session.commit()

    @classmethod
    def _base_query(cls) -> Query:
        """"
            SELECT s.set_id, s.set_name, s.set_description, c.category_name FROM sets as s
            LEFT JOIN public.categories c on c.category_id = s.set_category
            INNER JOIN public.users u on u.user_id = s.user_id
        """
        return db.session.query(
            Sets.set_id, Sets.set_name, Sets.set_description, Sets.set_modification_date,
            Categories.category_name, Subcategories.subcategory_name, Users.username, Sets.verified
        ).outerjoin(Categories, Categories.category_id == Sets.set_category) \
            .outerjoin(Subcategories, Subcategories.subcategory_id == Sets.set_subcategory) \
            .join(Users, Users.user_id == Sets.user_id)

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
            subcategory_id: str = "",
            user_id: str = "",
            folder_id: str = "",
            sort_by_date: bool = True,
            ascending: bool = False,
            search_terms: str | None = None,
    ) -> Pagination:
        """
        Retrieve a paginated list of sets from the database based on passed params for filtering and sorting

        Args:
            page (int): The page number to retrieve (default is 1).
            size (int): The number of sets per page (default is 20).
            category_id (str) If passed shows all sets with the given category,
            subcategory_id (str) If passed shows all sets with the given subcategory,
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

        if subcategory_id and category_id:
            query = query.filter(
                and_(Categories.category_id == category_id, Subcategories.subcategory_id == subcategory_id))

        if user_id:
            query = query.filter(Users.user_id == user_id)

        if folder_id:
            query = cls._sets_in_folder_query(folder_id)

        if sort_by_date:
            order_by_clause = (
                case((Sets.verified == True, 1), else_=0).desc(),
                desc(func.substring(Sets.set_id, 1, 10)) if not ascending else asc(func.substring(Sets.set_id, 1, 10))
            )

        else:
            if ascending:
                order_by_clause = (
                    case((Sets.verified == True, 1), else_=0).desc(),
                    asc(Sets.set_name),
                    asc(Sets.set_id)
                )

            else:
                order_by_clause = (
                    case((Sets.verified == True, 1), else_=0).desc(),
                    desc(Sets.set_name),
                    desc(Sets.set_id)
                )

        if search_terms:
            return cls.search_sets_flashcards(search_terms, page, size, category_id, subcategory_id)

        pagination: Pagination = query.order_by(*order_by_clause).paginate(page=page, per_page=size, error_out=True)
        return pagination

    @classmethod
    def search_sets_flashcards(cls, search_terms: str, page: int = 1, size: int = 20, category_id: str | None = None,
                               subcategory_id: str | None = None) -> Pagination:
        sets_query = db.session.query(Sets)

        if category_id:
            sets_query = sets_query.filter(Sets.set_category == category_id)

        if category_id and subcategory_id:
            sets_query = sets_query.filter(
                and_(Sets.set_category == category_id, Sets.set_subcategory == subcategory_id))

        sets_query = sets_query.outerjoin(Flashcards, Sets.set_id == Flashcards.set_id)
        sets_query = sets_query.options(
            joinedload(Sets.categories),
            joinedload(Sets.subcategories),
            joinedload(Sets.users),
        )
        sets_query = sets_query.add_columns(
            Flashcards,
            func.ts_rank(
                func.to_tsvector('simple', Sets.set_name + ' ' + Sets.set_description),
                func.plainto_tsquery('simple', search_terms)
            ).label('rank_sets'),
            func.ts_rank(
                func.to_tsvector('simple', Flashcards.term + ' ' + Flashcards.definition),
                func.plainto_tsquery('simple', search_terms)
            ).label('rank_flashcards')
        )
        sets_query = sets_query.filter(
            or_(
                func.to_tsvector('simple', Sets.set_name + ' ' + Sets.set_description).match(search_terms),
                func.to_tsvector('simple', Flashcards.term + ' ' + Flashcards.definition).match(search_terms)
            )
        )

        sets_results: Pagination = sets_query.distinct(Sets.set_id).order_by(Sets.set_id, desc('rank_sets'),
                                                                             desc('rank_flashcards')).paginate(
            page=page, per_page=size)

        return sets_results
