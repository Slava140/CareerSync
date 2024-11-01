from sqladmin import ModelView

from api.v1.profile.models.user import UserModel


class UserAdminView(ModelView, model=UserModel):
    name_plural = 'Users'
    name = 'User'
    column_default_sort = "created_at"
    column_list = [
        UserModel.first_name,
        UserModel.middle_name,
        UserModel.last_name,
        UserModel.role,
    ]
    column_details_exclude_list = [
        UserModel.created_at,
        UserModel.updated_at,
    ]

