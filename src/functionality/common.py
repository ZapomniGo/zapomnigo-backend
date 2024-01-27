from flask import Request

from src.utilities.parsers import arg_to_bool


class CommonFunctionality:
    @classmethod
    def get_pagination_params(cls, request: Request) -> tuple[int, int, bool, bool]:
        page = request.args.get('page', type=int)
        size = request.args.get('size', type=int)
        sort_by_date = request.args.get('sort_by_date', type=str, default='true')
        ascending = request.args.get('ascending', type=str, default='false')
        sort_by_date = arg_to_bool(sort_by_date)
        ascending = arg_to_bool(ascending)
        return page, size, sort_by_date, ascending
