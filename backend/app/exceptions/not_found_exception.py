from fastapi import status
from app.exceptions.api_exception import ApiException

class NotFoundException(ApiException):
    def __init__(self, resource:str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code= resource.upper()+"_NOT_FOUND",
            message=resource+" not found",
        )
