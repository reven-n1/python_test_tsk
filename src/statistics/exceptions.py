from fastapi import HTTPException


class ValidationError(HTTPException):
    def __init__(self, arg: str, typ: str, msg: str, e_typ: str):
        json_msg = {
            "loc": [
                f"{typ}",
                f"{arg}"
            ],
            "msg": f"{msg}",
            "type": f"{e_typ}"}
        super().__init__(422, [json_msg])


class NoContentFound(Exception):
    pass
