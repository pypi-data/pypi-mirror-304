from functools                                          import wraps
from fastapi                                            import Request
from cbr_shared.cbr_backend.session.CBR__Session_Auth   import cbr_session_auth
from osbot_utils.utils.Status                           import status_error

ERROR_MESSAGE__WITH_DB_USER__USER_NOT_FOUND      = "Session was found, but no valid user was mapped to it"

def with_db_user(func):
    @wraps(func)
    def wrapper(self, request: Request, *args, **kwargs):
        db_user = cbr_session_auth.user__from_request(request)
        if db_user:
            request.state.db_user = db_user                                 # Attach db_user to request.state
            return func(self, request, *args, **kwargs)
        return status_error(ERROR_MESSAGE__WITH_DB_USER__USER_NOT_FOUND)
    return wrapper
