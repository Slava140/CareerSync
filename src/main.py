from uuid import UUID

from fastapi import FastAPI, Request
from sqladmin import Admin

from admin_panel.views.user import UserAdminView

from api.routing import router as api_router
from api.v1.auth.schemas.refresh_session import RefreshSessionSchema
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


@app.get('/')
def main(request: Request, db_session: dbDependency, user: InUserSchema):
    return 'Ok'
