from flask import Request


class CommonFunctionality:
    @classmethod
    def get_pagination_params(cls, request: Request):
        page = request.args.get('page', type=int)
        size = request.args.get('size', type=int)
        return page, size
