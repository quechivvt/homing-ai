from fastapi import HTTPException, status


class ApiException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message,
            },
        )

