from uuid import UUID

from fastapi import FastAPI, Request
from sqladmin import Admin

from admin_panel.views.user import UserAdminView

from api.routing import router as api_router
from api.v1.auth.schemas.refresh_session import InRefreshSessionSchema
from api.v1.auth.schemas.token import FingerprintSchema
from api.v1.auth.services.refresh_session import RefreshSessionService
from api.v1.profile.schemas.user import InUserSchema
from api.v1.profile.services.user import UserService
from database import engine
from depends import dbDependency

app = FastAPI()
app.include_router(api_router)

admin = Admin(app, engine=engine)
admin.add_view(UserAdminView)


@app.post('/')
def main(request: Request, db_session: dbDependency, user: InUserSchema):
    return UserService.add_user(db_session, user)
    # fingerprint = FingerprintSchema(
    #     user_ip=request.client.host,
    #     user_agent=request.headers.get('user-agent'),
    #     accept_language=request.headers.get('accept-language')
    # )
    # return RefreshSessionService.add_session(db_session, user_uuid, fingerprint)
