from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Users


UserInSchema = pydantic_model_creator(#创建新用户
    Users, name="UserIn", exclude_readonly=True
)
UserOutSchema = pydantic_model_creator(#检索在我们的应用程序之外使用的用户信息，以便返回给最终用户
    Users, name="UserOut", exclude=["password", "created_at", "modified_at"]
)
UserDatabaseSchema = pydantic_model_creator(#检索应用程序中使用的用户信息，以验证用户
    Users, name="User", exclude=["created_at", "modified_at"]
)