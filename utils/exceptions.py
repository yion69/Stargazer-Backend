from postgrest.exceptions import APIError

class NotFoundError(APIError):
    def __init__(self, error='Resource Not Found'):
        super().__init__(error, status_code=404)