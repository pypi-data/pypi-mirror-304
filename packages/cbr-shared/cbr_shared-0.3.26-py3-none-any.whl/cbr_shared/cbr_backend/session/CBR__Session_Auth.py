from cbr_shared.cbr_backend.session.DB_Session   import DB_Session
from cbr_shared.cbr_backend.users.DB_User        import DB_User
from osbot_utils.base_classes.Type_Safe          import Type_Safe
from fastapi                                     import Request, HTTPException

COOKIE_NAME__SESSION_ID = 'CBR_TOKEN'           # todo: rename this to a better name (like CBR__SESSION_ID)

#api_key_header   = APIKeyHeader(name="Authorization", auto_error=False)


def cbr__fast_api__depends__admins_only(request: Request, session_id): #: str = Security(api_key_header)):
    if not request:
        raise HTTPException(status_code=501, detail="Request variable not available")
    cbr_session_auth.admins_only(request, session_id)


class CBR__Session_Auth(Type_Safe):

    def session__from_request(self, request:Request):
        session_id = self.session_id__from_request(request)
        if session_id:
            return self.session__from_session_id(session_id)

    def session__from_session_id(self, session_id: str):
        db_session = DB_Session(session_id)
        if db_session.exists():
            return db_session

    def session_data__from_request(self, request: Request):
        session = self.session__from_request(request)
        if session:
            return session.session_data()
        return {}

    def session_id__from_request(self, request: Request):
        if 'CBR_TOKEN' in request.cookies:
            session_id = request.cookies.get(COOKIE_NAME__SESSION_ID)
            if '|' in session_id:                                       # for the cases where the admin is impersonating a session ID
                session_id = session_id.split('|')[1]
            return session_id
        if 'authorization' in request.headers:
            return request.headers['authorization']

    def user__from_request(self, request: Request):
        db_session = self.session__from_request(request)
        if db_session:
            user_id = db_session.session_data__user_id()
            db_user = DB_User(user_id=user_id)
            if db_user.exists():
                return db_user

    def admins_only(self,request: Request, session_id): #: str = Security(api_key_header)):
        session_data = self.session_data__from_request(request)             # todo refactor this to use a Model for the data auth user_access mappings
        if session_data.get('data', {}).get('user_access', {}).get('is_admin'):
            return session_data
        else:
            raise HTTPException(status_code=401, detail="Unauthorized! Only admins can access this route")

cbr_session_auth = CBR__Session_Auth()