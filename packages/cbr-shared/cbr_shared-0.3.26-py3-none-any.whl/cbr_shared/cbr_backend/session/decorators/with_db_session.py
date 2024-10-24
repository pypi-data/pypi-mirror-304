from functools                                          import wraps
from typing                                             import TypeVar, Callable, Any
from fastapi                                            import Request
from cbr_shared.cbr_backend.session.CBR__Session_Auth   import cbr_session_auth
from osbot_utils.utils.Status                           import status_error

ERROR_MESSAGE__WITH_DB_SESSION__NOT_FOUND = "Session did not exist"

T = TypeVar('T')

def with_db_session(func: Callable[[Any, Request, ...], T]) -> Callable[[Any, Request, ...], T]:
    @wraps(func)
    def wrapper(self, request: Request, *args, **kwargs):
        try:
            db_session = cbr_session_auth.session__from_request(request)            # extract the session from a cookie or a header
            if db_session:                                                          # if we found a session
                request.state.db_session = db_session                               # attach it to request.state
                return func(self, request, *args, **kwargs)                         # and call the original function
            return status_error(ERROR_MESSAGE__WITH_DB_SESSION__NOT_FOUND)                   # return error when the session was not found
        except Exception as error:
            return status_error(f"Error processing session: {error}")
    return wrapper
