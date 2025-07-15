from postgrest.exceptions import APIError
class NotFoundError(APIError):
    def __init__(self, error='Resource Not Found'):
        super().__init__(error, status_code=404)


class JwtError(Exception):
    def __init__(self, message='JWT Token Error', status_code=500):
        super().__init__(message)
        self.status_code = status_code
        pass

class JwtExpiredError(JwtError):
    def __init__(self, message='JWT Token Expired', status_code=501):
        super().__init__(message, status_code)
        pass

class JwtInvalidTokenError(JwtError):
    def __init__(self, message='Invalid JWT Token', status_code=502):
        super().__init__(message, status_code)
        pass

