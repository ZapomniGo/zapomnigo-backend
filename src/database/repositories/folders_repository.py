from typing import List, Tuple

from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from flask_sqlalchemy.session import Session
from sqlalchemy import delete, desc, func, asc, and_, event, case

from src.database.models import Folders, FoldersSets, Categories, Users, Subcategories
from src.database.models.base import db


class FoldersRepository:

    @classmethod
    def get_folder_by_id(cls, folder_id: str) -> Folders | None:
        return db.session.query(Folders).filter_by(folder_id=folder_id).first()

    @classmethod
    def change_verified_status_folder(cls, folder: Folders, verified: bool) -> None:
        folder.verified = verified
        db.session.commit()

    @classmethod
    def _base_query(cls) -> Query:
        """"
        SELECT f.folder_id, f.folder_title, f.folder_description, f.folder_modification_date, c.category_name, u.username
        FROM folders as f
        LEFT JOIN public.categories c on c.category_id = f.category_id
        INNER JOIN public.users u on u.user_id = f.user_id
        """
        return db.session.query(
            Folders.folder_id, Folders.folder_title, Folders.folder_description, Folders.folder_modification_date,
            Categories.category_name, Subcategories.subcategory_name, Users.username, Folders.verified
        ).outerjoin(Categories, Categories.category_id == Folders.category_id) \
            .outerjoin(Subcategories, Subcategories.subcategory_id == Folders.subcategory_id) \
            .join(Users, Users.user_id == Folders.user_id)

    @classmethod
    def get_folder_info(cls, folder_id: str) -> List[Tuple[...]]:
        return cls._base_query().filter(Folders.folder_id == folder_id).all()

    @classmethod
    def get_all_folders(
            cls,
            page: int = 1,
            size: int = 20,
            category_id: str = "",
            subcategory_id: str = "",
            user_id: str = "",
            sort_by_date: bool = True,
            ascending: bool = False,
    ) -> Pagination:
        """
        Retrieve a paginated list of folders from the database based on passed params for filtering and sorting

        Args:
            page (int): The page number to retrieve (default is 1).
            size (int): The number of folders per page (default is 20).
            category_id (str) If passed shows all folders with the given category
            subcategory_id (str) If passed shows all folders with the given subcategory
            user_id (str): If provided, fetch folders associated with the specified user (default is an empty string).
            sort_by_date (bool): If True (default), the folders are ordered by creation date.
            ascending (bool): If True, the folders are ordered in ascending order, else in descending order.

        Returns:
            Pagination: A paginated result containing folders based on the specified parameters.
        """

        query = cls._base_query()

        if category_id:
            query = query.filter(Categories.category_id == category_id)

        if subcategory_id and category_id:
            query = query.filter(
                and_(Categories.category_id == category_id, Subcategories.subcategory_id == subcategory_id))

        if user_id:
            query = query.filter(Users.user_id == user_id)

        if sort_by_date:
            order_by_clause = (
                case((Folders.verified == True, 1), else_=0).desc(),
                desc(func.substring(Folders.folder_id, 1, 10)) if not ascending else asc(func.substring(Folders.folder_id, 1, 10))
            )

        else:
            if ascending:
                order_by_clause = (
                    case((Folders.verified == True, 1), else_=0).desc(),
                    asc(Folders.folder_title),
                    asc(Folders.folder_id)
                )

            else:
                order_by_clause = (
                    case((Folders.verified == True, 1), else_=0).desc(),
                    desc(Folders.folder_title),
                    desc(Folders.folder_id)
                )

        pagination: Pagination = query.order_by(*order_by_clause).paginate(page=page, per_page=size, error_out=True)

        return pagination

    @classmethod
    def delete_folders_sets_by_folder_id(cls, folder_id: str) -> None:
        db.session.execute(delete(FoldersSets).where(FoldersSets.folder_id == folder_id))
        db.session.commit()

    @event.listens_for(FoldersSets, 'after_delete')
    def receive_after_delete(mapper, connection, target):
        session: Session = Session.object_session(target)

        remaining = session.query(FoldersSets).filter_by(folder_id=target.folder_id).first()

        if remaining is None:
            session.execute(delete(Folders).where(Folders.folder_id == target.folder_id))
